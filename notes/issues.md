---
id: vkliqjlq7dnwnvcql3e9p7a
title: Issues
desc: ''
updated: 1682464418297
created: 1675740126695
---
## Separate cache for metadata annotations and comments

- This makes it difficult to link the different items together without recalling the `zot`.

## Sync and load must be different

- It makes sense to walk through the folder structure when first loading notes, but this model breaks when updating notes since any one of the items can be updated. E.g. an annotation can be updated without updating the metadata, but we still need to know the annotation's link to the metadata for file writing.
