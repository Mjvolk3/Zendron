import logging
from typing import Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyzotero import zotero

log = logging.getLogger(__name__)


# def get_metadatas(
#     zot: zotero.Zotero, collection: str = None, item_types: list = None
# ) -> list:
#     metadata_list = []
#     if collection is None:
#         for i in zot.everything(zot.items()):
#             if i["data"]["itemType"] in item_types:
#                 metadata_list.append(i)

#     if collection is not None:
#         collection_key = [
#             i for i in zot.collections() if i["data"]["name"] == collection
#         ][0]["key"]
#         items = zot.collection_items(collection_key)
#         for i in items:
#             if i["data"]["itemType"] in item_types:
#                 metadata_list.append(i)

#     log.info("Extracting Data Per entry")
#     return metadata_listhttps://github.com/Mjvolk3/Zendron/tree/main

def get_metadatas(zot, collection: str = None, item_types: list = None) -> list:
    def fetch_items():
        if collection is None:
            return zot.everything(zot.items())
        else:
            collection_key = [
                i for i in zot.collections() if i["data"]["name"] == collection
            ][0]["key"]
            return zot.collection_items(collection_key)
    
    def filter_item(item):
        return item["data"]["itemType"] in item_types
    
    items = fetch_items()
    filtered_items = []
    # Using ThreadPoolExecutor to parallelize API calls or processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Future-to-item mapping to preserve order
        future_to_item = {executor.submit(filter_item, item): item for item in items}
        
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            if future.result():
                filtered_items.append(item)
                
    log.info("Extracting Data Per entry")
    return filtered_items


def get_annotated_attachments(
    zot: zotero.Zotero, meta_key: Union[list[str], str]
) -> list[dict]:
    annotated_attachments = []
    if isinstance(meta_key, str):
        meta_key = [meta_key]
    for item in meta_key:
        data = zot.children(item)
        for item in data:
            try:
                if (
                    item["data"]["itemType"] == "attachment"
                    and item["data"]["contentType"] == "application/pdf"
                ):
                    data_temp = {}
                    data_temp["key"] = item["key"]
                    data_temp["version"] = item["version"]
                    data_temp["title"] = item["data"]["title"]
                    data_temp["zendron_title"] = set_title(
                        item["data"], item["data"]["title"]
                    )
                    annotated_attachments.append(data_temp)
            except KeyError:
                log.info("Ignoring attachments that aren't 'application/pdf'")
    return annotated_attachments


def get_attachments(zot: zotero.Zotero, meta_key: Union[list[str], str]) -> list[dict]:
    attachments = []
    data = zot.children(meta_key)
    for item in data:
        data_temp = {}
        data_temp["key"] = item["key"]
        data_temp["itemType"] = item["data"]["itemType"]
        try:
            data_temp["title"] = item["data"]["title"]
        except KeyError:
            data_temp["title"] = None
        data_temp["zendron_title"] = set_title(item["data"], data_temp["title"])
        attachments.append(data_temp)
    return attachments


# TODO remove if it works as a method in cache and it isn't being used anywhere else... might useful to hold onto
# def get_annotations(zot: zotero.Zotero, metadatas: list[dict]) -> list[dict]:
#     annotations = []
#     for meta in metadatas:
#         annotated_attachments = get_annotated_attachments(zot, meta["key"])
#         annotations_temp = []
#         for attach in annotated_attachments:
#             annotations_temp.extend(zot.children(attach["key"]))
#         annotations.extend(annotations_temp)
#     return annotations


def get_comments(
    zot: zotero.Zotero, metadata_list: list[dict], attachments: list[dict]
) -> list[dict]:
    comments = []
    attachments = []
    for metadata in metadata_list:
        attachments.extend(get_attachments(zot, metadata["key"]))

    comments = []
    comments.extend(
        [
            item
            for item in attachments
            if item["itemType"] == "note" and item["zendron_title"] == "zendron comment"
        ]
    )
    return comments


def set_title(data: dict, title: str) -> str:
    # def set_title(title: str = None, item_type: str = None) -> str:
    if data["itemType"] == "note":
        if data["note"] == "zendron comment":
            title = "zendron comment"
            return title
        else:
            return None
    prefix = title.split("_")[0]
    if prefix in [
        "supp",
        "Supp",
        "supplementary",
        "supp.",
        "supplementary-material",
        "supplementary-materials",
        "sup",
        "SI",
        "si",
    ]:
        title = prefix
    else:
        title = "annotations"
    return title


def main():
    pass


if __name__ == "__main__":
    main()
