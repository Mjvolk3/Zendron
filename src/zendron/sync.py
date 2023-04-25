import json
import logging
import os
import os.path as osp
import shutil
from collections import OrderedDict

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import Annotation, AnnotationsCompiler
from zendron.cache import Cache
from zendron.items import get_annotated_attachments, get_attachments, get_metadatas
from zendron.metadata import Metadata, MetadataCompiler

log = logging.getLogger(__name__)


# TODO when running sync make sure comments are always synced first... Probably go backwards in order of tree... annotations to metadata.
def remove_from_meta_queue(
    cache: Cache, metadata_list: list, dendron_limb: str, pod_path: str
):
    # Delete metadata that is not in the metadata_list.. These are items that have been remove from Zotero
    meta_remove_queue = list(
        set(cache.data.keys()) - set(i["key"] for i in metadata_list)
    )
    for meta_key in meta_remove_queue:
        dendron_limb_path = dendron_limb.replace(".", "/")
        delete_dir = osp.join(
            pod_path,
            dendron_limb_path,
            cache.data[meta_key]["title_dendron"],
        )
        delete_file_path = osp.join(
            pod_path,
            dendron_limb_path,
            cache.data[meta_key]["title_dendron"] + ".md",
        )
        user_file_path = osp.join(
            pod_path,
            dendron_limb_path,
            "user",
            cache.data[meta_key]["citation_key"] + ".md",
        )
        if osp.exists(delete_dir):
            log.info(f"Removing {delete_dir}")
            shutil.rmtree(delete_dir)
        if osp.exists(delete_file_path):
            log.info(f"Removing {delete_file_path}")
            os.remove(delete_file_path)
        if osp.exists(user_file_path):
            log.info(f"Removing {user_file_path}")
            os.remove(user_file_path)
        cache.delete_metadata(meta_key)


def sync_metadata(
    zot,
    metadata_list: list = None,
    dendron_limb: str = None,
    pod_path: str = None,
):
    cache = Cache(zot)
    cache.load()

    remove_from_meta_queue(cache, metadata_list, dendron_limb, pod_path)

    # Update metadata that is out versioned in cache
    meta_update_queue = []
    for meta in metadata_list:
        try:
            if meta["version"] > cache.data[meta["key"]]["version"]:
                meta_update_queue.append(meta)
        except KeyError:
            log.info(f"{meta['key']} not in cache")
            meta_update_queue.append(meta)

    for metadata in tqdm(meta_update_queue):
        attachments = get_attachments(zot, metadata["key"])
        metadata = Metadata(
            metadata,
            attachments,
            dendron_limb,
        )
        meta_compiler = MetadataCompiler(metadata, pod_path)
        meta_compiler.compile()
        meta_compiler.write()
        cache.update_metadata(metadata)
        print("")


# def sync_annotated_attachments(
#     zot,
#     all_annotated_attachments: list = None,
#     dendron_limb: str = None,
#     local_image_path: str = None,
#     pod_path: str = None,
# ):

#     cache = Cache(zot)
#     cache.load()

#     cached_annotated_attachments_temp = [
#         cache.data[k]["annotated_attachments"] for k, v in cache.data.items()
#     ]
#     cached_annotated_attachments = {}
#     for d in cached_annotated_attachments_temp:
#         cached_annotated_attachments.update(d)

#     for attach in all_annotated_attachments:
#         # for cache_att in cached_attachments
#         if (
#             attach["key"] in cached_annotated_attachments.keys()
#             and attach["version"]
#             > cached_annotated_attachments[attach["key"]]["version"]
#         ):
#             attach_update = attach
#         if attach["key"] not in cached_annotated_attachments.keys():
#             attach_update = attach

#         cache.update_annotated_attachment(attach_update)
#     print("")


def sync_annotations(
    zot,
    all_annotated_attachments: list = None,
    metadata_list: list = None,
    dendron_limb: str = None,
    local_image_path: str = None,
    pod_path: str = None,
):
    cache = Cache(zot)
    cache.load()

    annotations = []
    meta_keys = []
    for attach in all_annotated_attachments:
        annotations.extend(zot.children(attach["key"]))
        meta_keys.append(zot.item(attach["key"])["data"]["parentItem"])

    annot_queue = []
    meta_queue = []
    for annot, meta_key in zip(annotations, meta_keys):
        try:
            if annot["version"] > cache[annot["key"]]:
                annot_queue.append(annot)
                meta_queue.append(meta_key)
        except KeyError:
            log.info(f"{annot['key']} not in cache")
            annot_queue.append(annot)
            meta_queue.append(meta_key)

    # Rewriting the md file
    for annot, meta_key in zip(annot_queue, meta_queue):
        # IDEA this coupling to attachments is annoying. It might be better idea to give metadata access to zot.
        metadata = [i for i in metadata_list if i["key"] == meta_key][0]
        attachments = get_attachments(zot, meta_key)
        metadata = Metadata(
            metadata,
            attachments,
            dendron_limb,
        )
        annotated_attachments = get_annotated_attachments(zot, metadata.key)
        attach = [
            i for i in annotated_attachments if annot["data"]["parentItem"] == i["key"]
        ][0]
        # IDEA coupling to met metadata through metadata title is annoying. If Annotations had access to zot, it could get the metadata title, then title_dendron.
        annot_compiler = AnnotationsCompiler(
            attach["zendron_title"],
            metadata.title_dendron,
            local_image_path,
            dendron_limb,
            pod_path=pod_path,
        )
        annot_compiler.compile(zot.children(attach["key"]))
        annot_compiler.write()
        cache.update_annotation(annot["key"], annot["version"])


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf"), config_name="config"
)
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type
    zot = zotero.Zotero(library_id, library_type, api_key)
    metadata_list = get_metadatas(zot, cfg.collection, cfg.item_types)
    all_annotated_attachments = get_annotated_attachments(
        zot, [i["key"] for i in metadata_list]
    )
    log.info("Syncing metadata")
    sync_metadata(zot, metadata_list, cfg.dendron_limb, cfg.pod_path)
    sync_annotated_attachments(zot, all_annotated_attachments)
    # log.info("Syncing annotations")
    # sync_annotations(
    #     zot,
    #     all_annotated_attachments,
    #     metadata_list,
    #     cfg.dendron_limb,
    #     cfg.local_image_path,
    #     cfg.pod_path,
    # )
    print("")


if __name__ == "__main__":
    main()
