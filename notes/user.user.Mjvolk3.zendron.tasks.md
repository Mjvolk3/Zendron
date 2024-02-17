---
id: 7urrfe10vb294t7w5mgn9e2
title: tasks
desc: ''
updated: 1682803309990
created: 1675554123628
---
## Future

![[user.user.Mjvolk3.zendron.tasks.future#future]]

## 2023.04.29

- [ ] Fails when there is no pdf under file.
- [ ] Users notes will be deleted.
- [ ] Where to find the User ID, keys feeds api.
- [ ] Figure out automatic pinning. Describe how to setup.

## 2023.04.28

- [x] Tags for notes needs to throw a warning.
- 🔲 Where to find the User ID, keys feeds api.
- 🔲 Figure out automatic pinning. Describe how to setup.
- 🔲 Fails when there is no pdf under file.
- 🔲 Users notes will be deleted

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
- 🔲 Test and probably rewrite sync metadata → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Test and probably rewrite sync annotations → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Add delete note sync for annotations cache → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Add delete meta sync for metadata cache → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Add user note to meta sync. → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Test sync on metadata update and annotations update. → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Cache comments on sync. → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Simulate a workflow to make sure comments is working correctly. → moved to @user.Mjvolk3.zendron.tasks.future
- 🔲 Add cli. One primary function, sync, with additional functions, remove (comments flag`). → moved to @user.Mjvolk3.zendron.tasks.future

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
