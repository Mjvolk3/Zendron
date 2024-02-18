import logging

from omegaconf import DictConfig
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import AnnotationsCompiler
from zendron.cache import Cache, cache_difference
from zendron.comments import Comment, CommentCompiler
from zendron.items import (
    get_annotated_attachments,
    get_attachments,
    get_metadatas,
)
from zendron.metadata import Metadata, MetadataCompiler
from zendron.user_citation_key import UserCitationKey, UserCitationKeyCompiler
import hydra
import os
import os.path as osp 
from zendron import load
log = logging.getLogger(__name__)

# This is repeated in cache.py

# @hydra.main(
#     version_base=None,
#     config_path=osp.join(os.getcwd(), "conf", "zendron"),
#     config_name="config",
# )
def main(cfg: DictConfig):
    if not osp.exists(".zendron.cache.json"):
       load.main(cfg)
       return
   
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type
    zot = zotero.Zotero(library_id, library_type, api_key)
    
    log.info("Getting metadata from Zotero")
    new_cache = Cache(zot)
    metadata_list = get_metadatas(zot, cfg.collection, cfg.item_types)
    for metadata in tqdm(metadata_list):
        new_cache.add_metadata(metadata)
        attachments = get_attachments(zot, metadata["key"])
        annotated_attachments = get_annotated_attachments(zot, metadata["key"])
        for annot_attach in annotated_attachments:
            annotations = zot.children(annot_attach["key"])
            new_cache.add_annotations(annot_attach, annotations)
    
    old_cache = Cache(zot)
    old_cache.load()
    cache_diff = cache_difference(old_cache, new_cache)
    
    metadata_list = [zot.item(i["key"]) for i in cache_diff["new_metadata"]]
    cache = Cache(zot)
    log.info("Compiling new metadata")
    ######## same as load
    for metadata in tqdm(metadata_list):
        attachments = get_attachments(zot, metadata["key"])
        metadata = Metadata(
            metadata,
            attachments,
            cfg.dendron_limb,
        )
        meta_compiler = MetadataCompiler(metadata, cfg.pod_path)
        meta_compiler.compile()
        meta_compiler.write()
        user_citation_key = UserCitationKey(metadata, cfg.pod_path)
        user_citation_key_compiler = UserCitationKeyCompiler(user_citation_key)
        user_citation_key_compiler.compile()
        user_citation_key_compiler.write()
        
    def metadata_key_from_annotated_attachment(annotated_attachment):
        key = annotated_attachment['attachment_key']
        return zot.item(key)['links']['up']['href'].split('/')[-1]
    
    def get_title_dendron(metadata_key):
        # copied from [[Metadata|zendron.metadata]]
        title = zot.item(metadata_key)["data"]["title"]
        title = title.replace(":", "-")
        title_dendron = "-".join(title.split(" "))
        return title_dendron
    
    log.info("Compiling new annotated attachments")
    for annot_attach_key in tqdm(cache_diff["new_annotations"]):
        metadata_key = metadata_key_from_annotated_attachment(annot_attach_key)
        annotated_attachments = get_annotated_attachments(zot, metadata_key)
        for attach in annotated_attachments:
            annotations = zot.children(attach["key"])
            title_dendron = get_title_dendron(metadata_key)
            annot_compiler = AnnotationsCompiler(
                attach["zendron_title"],
                title_dendron,
                cfg.local_image_path,
                cfg.dendron_limb,
                cfg.pod_path,
            )
            annot_compiler.compile(annotations)
            annot_compiler.write()
        comment = Comment(zot, attachments)
        comment_compiler = CommentCompiler(
            comment, title_dendron, cfg.dendron_limb
        )
        comment_compiler.compile(comment)
        comment_compiler.write_comment()
    
    new_cache.write()
    if len(cache_diff["new_metadata"]) ==0 and len(cache_diff["new_annotations"]) ==0:
        log.info("No new metadata or annotations found.")
        return 0
    else:
        return 1
        

if __name__ == "__main__":
    main()
