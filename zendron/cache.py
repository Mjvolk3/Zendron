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
        self._data = None

    @property
    def data(self):
        if self._data is None:
            self._data = {}
        return self._data

    @property
    def cache_dir(self):
        if self._cache_dir is None:
            self._cache_dir = "zendron_cache"
            if not osp.exists(self._cache_dir):
                os.makedirs(self._cache_dir)
        return self._cache_dir

    @property
    def cache_file_path(self):
        if self._cache_file_path is None:
            self._cache_file_path = osp.join(self.cache_dir, "cache.json")
        return self._cache_file_path

    def load(self):
        if not osp.exists(self.cache_file_path):
            with open(self.cache_file_path, "w") as f:
                json.dump(self.data, f, indent=4)
        with open(self.cache_file_path, "r") as f:
            self._data = json.load(f)

    def add_metadata(self, metadata: Metadata):
        self.data[metadata.key] = {
            "version": metadata.metadata["data"]["version"],
            "title_dendron": metadata.title_dendron,
            "citation_key": metadata.citation_key,
            "annotated_attachments": {},
            "comment": {},
        }

    def add_annotated_attachment(self, attach_zen: dict):
        attachment = self.zot.item(attach_zen["key"])
        self.data[attachment["data"]["parentItem"]]["annotated_attachments"][
            attachment["key"]
        ] = {
            "version": attachment["version"],
            "title_dendron": attach_zen["zendron_title"],
            "annotations": {},
        }

    def add_annotations(self, annotations: list[dict]):
        # Disgusting nested loop 🤮...just refactor with the zot maybe?
        for meta in self.data.keys():
            if self.data[meta]["annotated_attachments"]:
                for attach in self.data[meta]["annotated_attachments"].keys():
                    for annot in annotations:
                        if annot["data"]["parentItem"] == attach:
                            self.data[meta]["annotated_attachments"][attach][
                                "annotations"
                            ][annot["key"]] = {
                                "version": annot["version"],
                            }

    def add_comment(self, comment: Comment):
        for meta in self.data.keys():
            if meta == comment.parentItem:
                self.data[meta]["comment"] = {
                    "version": comment.version,
                }

    def write(self):
        with open(self.cache_file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def update_metadata(self, metadata: Metadata):
        self.data[metadata.key]["version"] = metadata.metadata["data"]["version"]
        self.data[metadata.key]["title_dendron"] = metadata.title_dendron
        self.data[metadata.key]["citation_key"] = metadata.citation_key
        self.write()

    def update_annotated_attachment(self, attach_zen: dict):
        attachment = self.zot.item(attach_zen["key"])
        self.data[attachment["data"]["parentItem"]]["annotated_attachments"][
            attachment["key"]
        ]["version"] = attachment["version"]
        self.data[attachment["data"]["parentItem"]]["annotated_attachments"][
            attachment["key"]
        ]["title_dendron"] = attach_zen["zendron_title"]
        self.write()

    def delete_metadata(self, key: str):
        del self.data[key]
        self.write()


def main():
    pass


if __name__ == "__main__":
    main()
