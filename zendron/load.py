import logging

from omegaconf import DictConfig
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import AnnotationsCompiler
from zendron.cache import Cache
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

log = logging.getLogger(__name__)


@hydra.main(
    version_base=None,
    config_path=osp.join(os.getcwd(), "conf", "zendron"),
    config_name="config",
)
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type
    zot = zotero.Zotero(library_id, library_type, api_key)
    cache = Cache(zot)
    metadata_list = get_metadatas(zot, cfg.collection, cfg.item_types)
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
        cache.add_metadata(metadata.metadata)
        annotated_attachments = get_annotated_attachments(zot, metadata.key)
        for annot_attach in annotated_attachments:
            # TODO - remove after removal of deprecated cache
            # cache.add_annotated_attachment(attach)
            annotations = zot.children(annot_attach["key"])
            annot_compiler = AnnotationsCompiler(
                annot_attach["zendron_title"],
                metadata.title_dendron,
                cfg.local_image_path,
                cfg.dendron_limb,
                cfg.pod_path,
            )
            annot_compiler.compile(annotations)
            annot_compiler.write()
            cache.add_annotations(annot_attach, annotations)
        comment = Comment(zot, attachments)
        comment_compiler = CommentCompiler(
            comment, metadata.title_dendron, cfg.dendron_limb
        )
        comment_compiler.compile(comment)
        comment_compiler.write_comment()
        # TODO - remove after removal of deprecated comment
        # cache.add_comment(comment)
        cache.write()


if __name__ == "__main__":
    main()
