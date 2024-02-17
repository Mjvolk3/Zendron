## Future

- 🔮 If there are multiple collections or sub collections with the same name there needs to be an error or warning thrown.
- 🔮 If all data created are the same there will be duplicate title headings. This makes individual note refs impossible. For a two way sync it would be best if time created was modified, e.g. incremented by a second.
- 🔮 Fix importlib resources [[Configuration|issues.configuration]].
- 🔮 Figure out how to have a different default config for developing and a different one for releasing
- 🔮 In [[src/zendron/zendron-remove.py]] see what is using `subprocess` for file removal or a combination of `os` and `shutil`. `subprocess` must be used for dendron cli.
- 🔮 Add sync comments to load for a quick fix to make the package useful.
- 🔮 Test and probably rewrite sync metadata.
- 🔮 Test and probably rewrite sync annotations.
- 🔮 Add delete note sync for annotations cache.
- 🔮 Add delete meta sync for metadata cache.
- 🔮 Add user note to meta sync.
- 🔮 Test sync on metadata update and annotations update.
- 🔮 Cache comments on sync.
- 🔮 Simulate a workflow to make sure comments is working correctly.
- 🔮 Add cli. One primary function, sync, with additional functions, remove (comments flag`).
- 🔮 Add delete functionality to remove imported data.

## Far Future

- 🔮 `dacite`for dictionary to python dataclass. This could be used instead of my current method where I basically use a bunch of getter methods to pluck out data I am interested in while, adding necessary data for pod import.
