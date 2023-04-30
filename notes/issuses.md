---
id: 7g2c2qq7d38imc5pqcn3pcv
title: Issuses
desc: ''
updated: 1675724782122
created: 1675706716390
---
## Separate cache for metadata, annotations, and comments

- When an annotation is deleted we don't know which set annotated attachment to rewrite. It would be best if the cache was one file for this reason.

## Data objects

- Only data objects of a certain kind, dicts with the necessary keys, can be sent to zotero. If the dictionary returned from `zot.item(meta_key)` is modified it cannot be sent back to Zotero. For a future iteration of the dataclasses, there should be a `metadata.zotero`, and a `metadata.zendron`. All `metadata.zotero` should be able to be sent back to zotero, and all `metadata.zendron` should be used with the zendron application. This can be done for every data object that is important. Namely everything that is cached.

## Sync and Load must be different

- These [[src/zendron/sync.py]] and [[src/zendron/load.py]] must be structured different because the order in which the items are updated does not follow the hierarchy of the folder structure. This is fine for initialization but does not work after that.
