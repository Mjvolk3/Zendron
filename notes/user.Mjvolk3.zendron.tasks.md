---
id: bdjwj0s3mqeuuzxx9lq66ny
title: tasks
desc: ''
updated: 1708911657846
created: 1675554123628
---
## Future

![[user.Mjvolk3.zendron.tasks.future]]

## 2024.02.25

- [x] Figure out 2-way sync with load_since_cache.py
- [ ] Rebase and remove comment-sync branch

## 2024.02.24

- [x] 2-way comment sync with load
- 🔲 Figure out 2-way sync with load_since_cache.py

## 2024.02.23

- [x] Dendron cli latest does not work. 0.119.0 works. → There is already a [github issue](https://github.com/dendronhq/dendron/issues/3976) about this, added to README.
- [x] Install node from from <https://nodejs.org/en/> on macos and linux → added to README
- [x] Add pinning information. auto pin works for imports but you need to pin all files if you want to safely use lib.
- [x] setup api key → info for this already exists in README.
- [x] Show how to get the user amd group ids.  → info for this already exists in README.
- [x] `-remove` to `--remove` in readme
- [x] Common errors: `DendronError: vault with name <your-vault-name> not found`. This means that your vault name in `dendron.yml` was not set.
- [x] Look into comments → `comment-sync` branch

## 2024.02.18

- [x] Test it works from `pip` on.
- [x] Try to speed up get_metadatas → parallelized [[Load|zendron.load]] and [[Load_since_cache|zendron.load_since_cache]]

## 2024.02.17

- [x] WE BACK! refactor task notes.
- [x] Add front matter scripts and .env → also added the necessary workspace tasks → front matter works well.
- [x] Move zendron out of src, adjust pyproject.toml accordingly. → troubleshoot issue with pyproject
- [x] Remove bumpver with bumpver yaml and set up python-semantic-version. Add to requirements, add .github workflow.
- [x] Fix [[Remove|zendron.remove]] so it doesn't delete my task note → not sure what was happening before but works now.
- [x] Use `argparse` for remove command. → Since this works well we can just stick with this and hydra.
- [x] Move api config to `.env` → Not necessary since we .gitignore the config
- [x] Rewrite cache [[Cache|zendron.cache]]
- [x] Adding caching to main

## 2023.04.29

- [x] Users notes will be deleted. → Only deleting user notes based on cache. Additional notes further down hierarchy should not be deleted.
- [x] Fails when there is no pdf under file. → This no longer breaks `zendron`, still hacky [[src/zendron/metadata.py]]
- [x] Where to find the User ID, keys feeds api.
- [x] Figure out automatic pinning. Describe how to setup. → Added to [[README.md]].

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
- 🔲 Test and probably rewrite sync metadata → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Test and probably rewrite sync annotations → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Add delete note sync for annotations cache → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Add delete meta sync for metadata cache → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Add user note to meta sync. → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Test sync on metadata update and annotations update. → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Cache comments on sync. → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Simulate a workflow to make sure comments is working correctly. → moved to @Mjvolk3.zendron.tasks.future
- 🔲 Add cli. One primary function, sync, with additional functions, remove (comments flag`). → moved to @Mjvolk3.zendron.tasks.future

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
