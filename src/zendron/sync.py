import json
import logging
import os.path as osp
from collections import OrderedDict

import bibtexparser
import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron.resync import AnnotationsCompiler, Metadata, MetadataCompiler

# TODO only handled added content, not deleted content
# set logger
log = logging.getLogger(__name__)


def metadata(zot):
    # TODO adding in books, preprints, collections, etc.
    itemType = ["journalArticle"]
    itemType = (" || ").join(itemType)
    # cache #TODO decorator cache
    if osp.exists("zendron_cache/metadata_cache.json"):
        with open("zendron_cache/metadata_cache.json", "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    # update new metadata
    metadata_list = []
    for i in zot.items(itemType=itemType):
        try:
            if i["version"] > cache[i["key"]]:
                metadata_list.append(i)
        except KeyError:
            log.info(f"{i['key']} not in cache")
            metadata_list.append(i)

    for metadata in tqdm(metadata_list):
        log.info("Extracting Data Per entry")
        # metadata
        meta = Metadata(metadata)
        meta_compiler = MetadataCompiler(meta.title_dendron)
        meta_compiler.compile(meta)
        meta_compiler.write_metadata()
    with open("zendron_cache/metadata_cache.json", "w") as f:
        cache = zot.item_versions(itemType=itemType)
        json.dump(cache, f, indent=4)


def annotations(zot):
    itemType = ["annotation"]
    # cache
    if osp.exists("zendron_cache/annotations_cache.json"):
        with open("zendron_cache/annotations_cache.json", "r") as f:
            cache = json.load(f)
    else:
        cache = {}
    # update new annotations
    pdf_attachment_id_list = []
    metadata_id_list = []
    for i in zot.items(itemType=itemType):
        pdf_attachment_id = i["data"]["parentItem"].split("/")[-1]
        metadata_id_list.append(
            zot.item(pdf_attachment_id)["data"]["parentItem"].split("/")[-1]
        )
        try:
            if i["version"] > cache[i["key"]]:
                pdf_attachment_id_list.append(pdf_attachment_id)
        except KeyError:
            log.info(f"{i['key']} not in cache")
            pdf_attachment_id_list.append(pdf_attachment_id)
    # zip pdf_attachment_id_list and metadata_id_list into a list of tuples
    attach_meta = list(zip(pdf_attachment_id_list, metadata_id_list))
    attach_meta = list(OrderedDict.fromkeys(attach_meta))

    for pdf_attachment_id, metadata_id in tqdm(attach_meta):
        # annotations
        annotations = zot.children(pdf_attachment_id)
        metadata = zot.item(metadata_id)
        meta = Metadata(metadata)
        annot_compiler = AnnotationsCompiler(meta.title_dendron)
        annot_compiler.compile(annotations)
        annot_compiler.write_annotations()
    with open("zendron_cache/annotations_cache.json", "w") as f:
        cache = zot.item_versions(itemType=itemType)
        json.dump(cache, f, indent=4)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    # TODO add to configs
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    zot = zotero.Zotero(library_id, library_type, api_key)
    # TODO implement collections
    if cfg.collection is not None:
        collection = [
            i for i in zot.collections() if i["data"]["name"] == cfg.collection
        ]
    log.info("Syncing metadata")
    metadata(zot)
    log.info("Syncing annotations")
    annotations(zot)


if __name__ == "__main__":
    main()
