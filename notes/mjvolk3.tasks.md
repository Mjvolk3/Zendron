---
id: bdjwj0s3mqeuuzxx9lq66ny
title: Tasks
desc: ''
updated: 1682464423221
created: 1675554123628
---
## Future

![[mjvolk3.tasks.future#future]]

## 2023.02.06

- [x] Clean up [[src/zendron/sync.py]]. Theres is some confusion with `annot`, `annotated_attachment`, and `annotations`, specifically in sync_annotations.
- [x] Rewrite cache.[[issuses#separate-cache-for-metadata-annotations-and-comments]]
- [x] Try structuring [[src/zendron/sync.py]] like [[src/zendron/load.py]]. → Doesn't work [[issuses#sync-and-load-must-be-different]]
- 🔲 Test and probably rewrite sync metadata → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Test and probably rewrite sync annotations → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Add delete note sync for annotations cache → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Add delete meta sync for metadata cache → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Add user note to meta sync. → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Test sync on metadata update and annotations update. → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Cache comments on sync. → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Simulate a workflow to make sure comments is working correctly. → moved to [[Future|mjvolk3.tasks.future#future]]
- 🔲 Add cli. One primary function, sync, with additional functions, remove (comments flag`). → moved to [[Future|mjvolk3.tasks.future#future]]

## 2023.02.05

- [x] Cache metadata on sync.
- [x] Cache annotations on sync.
- 🔲 Cache comments on sync.
- 🔲 Add cli.

## 2023.02.04

- [x] Cache classes for annotations, comments, metadata.
- [x] Cache initialization on load.
- 🔲 Cache annotations on sync.
- 🔲 Cache comments on sync.
R
