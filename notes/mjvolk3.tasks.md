---
id: bdjwj0s3mqeuuzxx9lq66ny
title: Tasks
desc: ''
updated: 1682721968974
created: 1675554123628
---
## Future

![[mjvolk3.tasks.future#future]]

## 2023.04.28

- [ ] Where to find the User ID, keys feeds api.
- [ ] Figure out automatic pinning. Describe how to setup.
- [ ] Fails when there is no pdf under file.
- [ ] Tags for notes needs to throw a warning.
- [ ] Users notes will be deleted

## 2023.04.27

- [x] Published mvp.

## 2023.04.25

- [x] Fix citation key.
- [x] Remove script [[src/zendron/zendron-remove.py]].
- [x] `Zendron-remove` endpoint.
- [x] Test out @mjvolk3 recreation after deletion.
- [x] Test @kipfVariationalGraphAutoEncoders2016 is recreated since it is referenced in [[Introduction|paper.Introduction]]
- [x] Check `Zendron-remove` endpoint.
- [x] Publish to PyPI.

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
