# zendron/cache
# [[zendron.cache]]
# https://github.com/Mjvolk3/Zendron/tree/main/zendron/cache
# Test file: tests/zendron/test_cache.py

import json
import logging
import os
import os.path as osp
import typing
from typing import Union

from pyzotero import zotero
from pyzotero.zotero_errors import ResourceNotFound

from zendron.annotations import Annotation
from zendron.comments import Comment
from zendron.items import get_annotated_attachments, get_attachments, get_metadatas
from zendron.metadata import Metadata

log = logging.getLogger(__name__)


class Cache:
    def __init__(self, zot: zotero.Zotero = None, **kwargs):
        self.zot = zot
        self._cache_dir = "zendron_cache"
        if not osp.exists(self._cache_dir):
            os.makedirs(self._cache_dir)
        self._cache_file_path = None
        self._annotations_cache = None
        self._metadata_cache = None

    @property
    def annotations_cache(self):
        if self._annotations_cache is None:
            self._annotations_cache = []
        return self._annotations_cache

    @property
    def metadata_cache(self):
        if self._metadata_cache is None:
            self._metadata_cache = []
        return self._metadata_cache

    @property
    def cache_file_path(self):
        if self._cache_file_path is None:
            self._cache_file_path = ".zendron.cache.json"
        return self._cache_file_path

    def load(self):
        if osp.exists(self.cache_file_path):
            with open(self.cache_file_path, "r") as f:
                data = json.load(f)
                self._metadata_cache = data["metadata"]
                self._annotations_cache = data["annotations"]
            return True
        return False

    # This is repeated in load_since_cache.py
    
    def get_citation_key(self, metadata):
        extras = metadata["data"]["extra"].split("\n")
        citation_key = [i for i in extras if "Citation Key" in i]
        citation_key = citation_key[0].split("Citation Key: ")[-1]
        return citation_key

    def add_metadata(self, metadata):
        self.metadata_cache.append(
            {
                "citation_key": self.get_citation_key(metadata),
                "key": metadata["key"],
                "date_modified": metadata["data"]["dateModified"],
            }
        )

    # def add_annotated_attachment(self, attach_zen: dict):
    #     attachment = self.zot.item(attach_zen["key"])
    #     self.data[attachment["data"]["parentItem"]]["annotated_attachments"][
    #         attachment["key"]
    #     ] = {
    #         "version": attachment["version"],
    #         "title_dendron": attach_zen["zendron_title"],
    #         "annotations": {},
    #     }

    def add_annotations(self, annotated_attachment, annotations: list[dict]):
        annotation_keys = []
        # Initialize date_modified with the date of the first annotation if annotations list is not empty
        date_modified = annotations[0]["data"]["dateModified"] if annotations else "1900-01-01T00:00:00Z"

        for annot in annotations:
            # Assuming annotations could be unsorted or you want the earliest date
            annotation_keys.append(annot["key"])
            current_date_modified = annot["data"]["dateModified"]
            if current_date_modified < date_modified:
                date_modified = current_date_modified

        self.annotations_cache.append(
            {
                "attachment_key": annotated_attachment["key"],
                "annotation_keys": annotation_keys,
                "date_modified": date_modified,
            }
        )

    def write(self):
        data = {
            "annotations": self.annotations_cache,
            "metadata": self.metadata_cache,
        }
        with open(self.cache_file_path, "w") as f:
            json.dump(data, f, indent=4)

    def update_metadata(self, metadata: Metadata):
        pass

    def update_annotated_attachment(self, attach_zen: dict):
        pass

    def delete_metadata(self, key: str):
        del self.data[key]
        self.write()


def cache_difference(old_cache: Cache, new_cache: Cache) -> dict:
    """
    Computes the difference between two Cache instances based on new attachment keys,
    unmatched sets of annotation keys, or more recent date_modified for annotations.
    """
    def diff_annotations(old_annotations, new_annotations):
        # Convert list to dict for easy lookup by attachment_key
        old_dict = {item['attachment_key']: item for item in old_annotations}
        new_diff = []

        for new_item in new_annotations:
            old_item = old_dict.get(new_item['attachment_key'])
            # Case 1: New attachment key
            if not old_item:
                new_diff.append(new_item)
                continue

            # Case 2: Unmatched set of annotation keys
            if set(old_item['annotation_keys']) != set(new_item['annotation_keys']):
                new_diff.append(new_item)
                continue

            # Case 3: More recent date_modified
            if old_item['date_modified'] < new_item['date_modified']:
                new_diff.append(new_item)

        return new_diff

    new_metadata_diff = [
        item for item in new_cache.metadata_cache
        if item not in old_cache.metadata_cache
    ]

    new_annotations_diff = diff_annotations(old_cache.annotations_cache, new_cache.annotations_cache)

    return {
        "new_metadata": new_metadata_diff,
        "new_annotations": new_annotations_diff,
    }


def main():
    pass


if __name__ == "__main__":
    main()
