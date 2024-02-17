import json
import logging
import os
import os.path as osp
from dataclasses import dataclass, field
from datetime import datetime

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import AnnotationsCompiler
from zendron.cache import Cache
from zendron.comments import Comment, CommentCompiler
from zendron.items import (
    get_annotated_attachments,
    get_attachments,
    get_comments,
    get_metadatas,
)
from zendron.metadata import Metadata, MetadataCompiler
from zendron.user_citation_key import UserCitationKey, UserCitationKeyCompiler

log = logging.getLogger(__name__)


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
        cache.add_metadata(metadata)
        # TODO rename to something like annotated_attachments. This is not a list of the annotations themselves, but the attachment that contains the annotations.
        annotated_attachments = get_annotated_attachments(zot, metadata.key)
        for attach in annotated_attachments:
            cache.add_annotated_attachment(attach)
            annotations = zot.children(attach["key"])
            annot_compiler = AnnotationsCompiler(
                attach["zendron_title"],
                metadata.title_dendron,
                cfg.local_image_path,
                cfg.dendron_limb,
                cfg.pod_path,
            )
            annot_compiler.compile(annotations)
            annot_compiler.write()
            cache.add_annotations(annotations)
        comment = Comment(zot, attachments)
        comment_compiler = CommentCompiler(
            comment, metadata.title_dendron, cfg.dendron_limb
        )
        comment_compiler.compile(comment)
        comment_compiler.write_comment()
        cache.add_comment(comment)
        cache.write()


if __name__ == "__main__":
    main()
