# zendron/load
# [[zendron.load]]
# https://github.com/Mjvolk3/Zendron/tree/main/zendron/load
# Test file: tests/zendron/test_load.py

import logging
import os
import os.path as osp
from concurrent.futures import ThreadPoolExecutor, as_completed
from omegaconf import DictConfig
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import AnnotationsCompiler
from zendron.cache import Cache
from zendron.comments import Comment, CommentCompiler, push_comment
from zendron.items import get_annotated_attachments, get_attachments, get_metadatas
from zendron.metadata import Metadata, MetadataCompiler
from zendron.user_citation_key import UserCitationKey, UserCitationKeyCompiler
import hydra

log = logging.getLogger(__name__)

def process_metadata(metadata, zot, cfg, cache):
    attachments = get_attachments(zot, metadata["key"])
    metadata_obj = Metadata(metadata, attachments, cfg.dendron_limb)
    meta_compiler = MetadataCompiler(metadata_obj, cfg.pod_path)
    meta_compiler.compile()
    meta_compiler.write()
    user_citation_key = UserCitationKey(metadata_obj, cfg.pod_path)
    user_citation_key_compiler = UserCitationKeyCompiler(user_citation_key)
    user_citation_key_compiler.compile()
    user_citation_key_compiler.write()
    cache.add_metadata(metadata_obj.metadata)
    annotated_attachments = get_annotated_attachments(zot, metadata_obj.key)
    for annot_attach in annotated_attachments:
        annotations = zot.children(annot_attach["key"])
        annot_compiler = AnnotationsCompiler(
            annot_attach["zendron_title"],
            metadata_obj.title_dendron,
            cfg.local_image_path,
            cfg.dendron_limb,
            cfg.pod_path,
        )
        annot_compiler.compile(annotations)
        annot_compiler.write()
        cache.add_annotations(annot_attach, annotations)
    comment = Comment(zot, attachments, metadata_obj.title_dendron, cfg.dendron_limb)
    comment_compiler = CommentCompiler(comment)
    comment_compiler.compile()
    comment_compiler.write_comment()
    push_comment(zot, comment)
    # Additional operations if needed
    return True  # Placeholder return value

@hydra.main(version_base=None, config_path=osp.join(os.getcwd(), "conf", "zendron"), config_name="config")
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type
    zot = zotero.Zotero(library_id, library_type, api_key)
    cache = Cache(zot)
    metadata_list = get_metadatas(zot, cfg.collection, cfg.item_types)
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_metadata, metadata, zot, cfg, cache) for metadata in metadata_list]
        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()  # Placeholder for any result handling
    
    cache.write()

if __name__ == "__main__":
    main()
