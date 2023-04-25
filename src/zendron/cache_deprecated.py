import json
import logging
import os
import os.path as osp
from typing import Union

from pyzotero import zotero
from pyzotero.zotero_errors import ResourceNotFound

from zendron.items import get_annotated_attachments, get_attachments, get_metadatas

log = logging.getLogger(__name__)

from abc import ABC, abstractmethod, abstractproperty


class Cache(ABC):
    def __init__(self, zot: zotero.Zotero = None, **kwargs):
        self.zot = zot
        self._cache_dir = "zendron_cache"
        self._cache_file_path = None

    @property
    def cache_dir(self):
        if self._cache_dir is None:
            self._cache_dir = "zendron_cache"
            if not osp.exists(self._cache_dir):
                os.makedirs(self._cache_dir)
        return self._cache_dir

    def load(self):
        if osp.exists(self.cache_file_path):
            with open(self.cache_file_path, "r") as f:
                cache_temp = json.load(f)
            cache = cache_temp.copy()
            for k in cache_temp.keys():
                try:
                    self.zot.item(k)
                except ResourceNotFound:
                    log.info("Items have been deleted from Zotero.")
                    del cache[k]
            with open(self.cache_file_path, "w") as f:
                json.dump(cache, f, indent=4)
            return cache
        else:
            cache = {}
            return cache

    @abstractproperty
    def cache_file_path(self):
        pass

    @abstractmethod
    def initialize(self) -> dict:
        pass

    @abstractmethod
    def update(self) -> dict:
        pass


class MetadataCache(Cache):
    def __init__(
        self,
        zot: zotero.Zotero = None,
        item_types: list = None,
        **kwargs,
    ):
        super().__init__(zot, **kwargs)
        self.item_types = (" || ").join(item_types)

    @property
    def cache_file_path(self):
        if self._cache_file_path is None:
            self._cache_file_path = osp.join(self.cache_dir, "metadata_cache.json")
        return self._cache_file_path

    def initialize(self, metadata_list: list[dict]) -> dict:
        with open(self.cache_file_path, "w") as f:
            cache = self.zot.item_versions(itemType=self.item_types)
            cache = self._metadata_filter(cache, metadata_list)
            json.dump(cache, f, indent=4)
            return cache

    def update(self, metadata_list: list[dict]) -> dict:
        with open(self.cache_file_path, "w") as f:
            cache = self.zot.item_versions(itemType=self.item_types)
            cache = self._metadata_filter(cache, metadata_list)
            json.dump(cache, f, indent=4)

    def _metadata_filter(self, cache: dict, metadata_list: list[dict]):
        meta_keys = [item["key"] for item in metadata_list]
        cache = {key: cache[key] for key in meta_keys}
        return cache


class AnnotationsCache(Cache):
    def __init__(
        self,
        zot: zotero.Zotero = None,
        **kwargs,
    ):
        super().__init__(zot, **kwargs)
        self.item_type = ["annotation"]

    @property
    def cache_file_path(self):
        if self._cache_file_path is None:
            self._cache_file_path = osp.join(self.cache_dir, "annotations_cache.json")
        return self._cache_file_path

    def initialize(self, metadatas: list[dict]) -> dict:
        with open(osp.join(self.cache_dir, "annotations_cache.json"), "w") as f:
            cache = self.zot.item_versions(itemType=self.item_type)
            annotations = self._get_annotations(self.zot, metadatas)
            cache = self._annotations_filter(cache, annotations)
            json.dump(cache, f, indent=4)
            return cache

    def update(self, metadatas: list[dict]) -> dict:
        with open(self.cache_file_path, "w") as f:
            cache = self.zot.item_versions(itemType=self.item_type)
            annotations = self._get_annotations(self.zot, metadatas)
            cache = self._annotations_filter(cache, annotations)
            json.dump(cache, f, indent=4)

    def _annotations_filter(self, cache: dict, annotations: list[dict]):
        annot_keys = [item["key"] for item in annotations]
        cache = {key: cache[key] for key in annot_keys}
        return cache

    def _get_annotations(self, zot: zotero.Zotero, metadatas: list[dict]) -> list[dict]:
        annotations = []
        for meta in metadatas:
            annotated_attachments = get_annotated_attachments(zot, meta["key"])
            annotations_temp = []
            for attach in annotated_attachments:
                annotations_temp.extend(zot.children(attach["key"]))
            annotations.extend(annotations_temp)
        return annotations


class CommentsCache(Cache):
    def __init__(
        self,
        zot: zotero.Zotero = None,
        **kwargs,
    ):
        super().__init__(zot, **kwargs)
        self.cache_file = "comments_cache.json"

    def initialize(self, comments: list[dict]) -> dict:
        itemType = ["note"]
        with open(osp.join(self.cache_dir, "comments_cache.json"), "w") as f:
            cache = self.zot.item_versions(itemType=itemType)
            comment_keys = [item["key"] for item in comments]
            cache = {key: cache[key] for key in comment_keys}
            json.dump(cache, f, indent=4)
        pass

    def update(self) -> dict:
        pass

    def load(self) -> dict:
        pass


# IDEA class cache?
def init(name: str = None):
    if name == "annotations":
        if osp.exists("zendron_cache/annotations_cache.json"):
            with open("zendron_cache/annotations_cache.json", "r") as f:
                cache = json.load(f)
        else:
            cache = {}
        return cache
    elif name == "metadata":
        if osp.exists("zendron_cache/metadata_cache.json"):
            with open("zendron_cache/metadata_cache.json", "r") as f:
                cache = json.load(f)
        else:
            cache = {}
        return cache
    elif name == "comments":
        if osp.exists("zendron_cache/comments_cache.json"):
            with open("zendron_cache/comments_cache.json", "r") as f:
                cache = json.load(f)
        else:
            cache = {}
        pass
