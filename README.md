<p align="center">
  <img src="https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/drawio/logo.drawio.png" />
</p>

[![PyPI version](https://badge.fury.io/py/zendron.svg)](https://badge.fury.io/py/zendron)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/michaelvolk)

## Showcase

Here we show how `zendron` enables a writing workflow from within VsCode.

![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/videos/gif/zendron-test_2.gif)

1. First we show how you can structure a paper using note references in Dendron.
2. Install `zendron` and import references from the relevant Zotero library.
3. Cite while you write, and view all relevant Zotero metadata, annotations, and comment notes with hover.
4. Compile paper to `.docx`, `.pdf`, and `.html` with Pandoc.
5. Find relevant papers via VsCode search.

## Introduction

- This package was developed for porting Zotero annotations and metadata to markdown. This is made possible with [pyzotero](https://pyzotero.readthedocs.io/en/latest/). These markdown notes are then brought into a [Dendron](https://www.dendron.so/) hierarchy for integration with vault notes. Zendron is designed to be used with [Visual Studio Code](https://code.visualstudio.com/) but is editor agnostic... in theory. The end goal is to get a two way sync between notes in Zotero and notes in Dendron, but this has some difficulties and limitations. For now only a one way sync from Zotero to Dendron is supported.

## Install Instructions

- It is recommended to build a virtual environment for installation. I've used  [conda env](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) during development.

- Install [Dendron CLI](https://wiki.dendron.so/notes/RjBkTbGuKCXJNuE4dyV6G/) this is needed for note import into Dendron.
  - [Install node js](https://nodejs.org/en/download)
    - For more information you can check out [Dendron node install instruction](https://wiki.dendron.so/notes/RjBkTbGuKCXJNuE4dyV6G/)
  - `npm install -g @dendronhq/dendron-cli@0.119.0`
    - I use the global flag, but you can alternativley install a specific version for a given workspace.
    - Newer version are not working, waiting on any response to [github issue](https://github.com/dendronhq/dendron/issues/3976)
- Install the zendron
  - `python -m pip install zendron`

## Zotero Local Setup

- To start you need [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/installation/)
  - This allows pinning of bibtex keys. A stable bibtex key is necessary for predictable behavior within `zendron.`
- Go to `Zotero > Settings... > Advanced > General > Config Editor`![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.zotero-config-editor.png)
- Accept the risks.
![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.zotero-config-editor-accept-risks.png)
- In the Search, type `autoPinDelay` and change the integer value from 0 (default) to 1. Click OK.
![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.autoPinDelay-update.png)
- This will automatically pin any new publications coming into your zotero database. For previous citations that are not yet pinned, you can highlight all metadata, right click and select `Better BibTex > Pin BibTeX key`. This will make your entries compatible with Zendron. This is a one time thing, after setting the `autoPinDelay`, you won't need to worry about this.

## Zotero API key

- Visit here to setup a [Zotero API key](https://www.zotero.org/settings/keys).
- We recommend setting up your Zotero API key with the following settings to allow for full functionality.
  - Personal Library
    - [x] Allow library access.
    - [x] Allow notes access.
    - [x] Allow write access.
  - Default Group Permissions
    - [x] Read/Write

![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zotero.api-key.md.zotero-api-key.png)

- This key can then be copy-pasted in the configuration file, `"config.yaml"`. You should add your key to `.gitignore` to prevent others from accessing your Zotoero database. If the key is lost you can always generate a new one.

## Basic Usage

🚨 **THE MOST IMPORTANT THING** 🚨 - When you any `zendron` command make sure that you have a clean working directory. Meaning run `git status`, and make sure there are no untracked files or files to commit. This makes it very easy to revert modifications made by `zendron` while we still work out the kinks.

There is 1 command, and 3 optional flags.

- `zendron`
  - This command should only be run in the root directory of the workspace.
  - This command imports notes according to a defined [config.yaml](https://github.com/Mjvolk3/Zendron/raw/main/conf/config.yaml). Once the command is run the first time the user needs to modify their configuration `./conf/zendron/config.yaml`. All required configs are marked with a comment `# STARTER CONFIG` upon initialization.
  - Notes are imported with a `## Time Created` heading. This allows for stable reference from other notes, within the note vault. We autogenerate a `*.comments.md` that should be used for taking any additional notes within Dendron. Additional notes taken within the meta data file (`notes/zendron.import.<paper-title>.md`), or the `*.annotations.md` will be overwritten after running `zendron -rm` or `zendron -nc`. All files downstream of `.import` except `*.comments.md` should be treated as read only.
  - Upon import, notes and tags are left as stubs. To create these notes run `> Dendron: Doctor` then `createMissingLinkedNotes`. It is best practice to correct tag warnings before doing this. We warn on malformed tag imports. We could reform tags and sync to Zotero if there is interest.
  - After running this command it is best to run `Dendron: Reload Index` from the command palette.
- `zendron -h` or `zendron --help`
  - Help message that shows availbe commands and suggsetions for when running `zendron`.
- `zendron -rm` or `zendron --remove`
  - ⚠️ This command removes imported notes and associated links. This command works by removing all notes downstream to `dendron_limb`. There is some difficulty removing other files created because these are separate from the `dendron_limb`. These files include `user.*.md`, which comes from bibtex keys, and `tags.*.md` which come from metadata and annotation tags. For now, we don't remove tags, but we do remove bibex keys (`<user.bibtex_key>.md`).
  - ⚠️I have to say it again, don't put other notes downstream of the zendron limb. They will be deleted.
  - We don't delete imported tags because they are too difficult to track consistently.
- `zendron -drm` or `zendron --dry-remove`
  - A dry removal so you can see what file will be deleted without deleting them.
- `zendron -nc` or `zendron --no-cache`
  - This is zendron sync without caching. This good to run if you interrupted your import for some reason and need a fresh clean import. If your zendron notes are misbehaving try this command. It will be slower since there is no caching.
  - After running this command it is best to run `Dendron: Reload Index` from the command palette.

## Zotero and File Import Configuration

All zendron configuration is handled in [config.yaml](https://github.com/Mjvolk3/Zendron/blob/main/zendron/conf/zendron/config_template.yaml). Upon initialization it will show in `"config/zendron/config.yaml"`.

```yml
library_id : 4932032 # Zotero library ID
library_type : group # [user, group] library
api_key : FoCauOvWMlNdYmpYuY5JplTw # Zotero API key
collection: null # Name of Zotero Collection, null for entire library
local_image_path: /Users/<username>/Zotero/cache # Local path for importing annotated images
```

[default.yaml](https://github.com/Mjvolk3/Zendron/blob/main/zendron/conf/zendron/config_template.yaml)

```yaml
item_types: [journalArticle, book, preprint, conferencePaper, report] # List of item types according to [pyzotero](https://pyzotero.readthedocs.io/en/latest/). Kept here for beginner simplicity.
dendron_limb: zendron.import # Dendron import limb e.g. zendron.import.paper-title.annotations.md. KEEPING here for now since hasn't been tested.
zotero_comment_title: zendron comment # needed for eventual 2-way sync. HERE for now.
pod_path: zendron_pod # Name of dendron pod, removed after completion of import. Key for non dendron user import. Not implemented yet.
```

- `library_id` - Integer identifier of library. This is the number that matches the name of a library.
  - [User ID](https://www.zotero.org/settings/keys). For a user library it you will see something like `"Your userID for use in API calls is 1234567"`
  - For group ID visit [Zotero Groups](https://www.zotero.org/groups/), click on your desired group, and copy the id from the URL. For instance I have this library. `"https://www.zotero.org/groups/4932032/zendron/library"`, and 4932032 is the `library_id`.
- `library_type`: `group` for group libraries and `user` for user library.
- `api_key`: Use the API Key obtained from [Zotero API KEY](README.md#zotero-api-key).
- `collection`: This can be the name of any collection or subcollection in the specificed library. If there are multiple collections or sub collections with the same name, the import will arbitrarily choose one. To make sure you are importing the desired collection, make sure the name of the collection is unique in the Zotero library. Subcollections of a collection will not be imported, this is by design according to how zotero handles subcollections and collections.
- `item_types`: Zotero item types to import according to [pyzotero](https://pyzotero.readthedocs.io/en/latest/) syntax.
`local_image_path`: Path to annotated images. `/Users/<username>/Zotero/cache` is the default path on MacOS. It just needs to end in `cache`.
- `dendron_limb`: This is the period deliminated hierarchy prefix to all file imports for Dendron, e.g. `root.zotero.import.<paper_title>.annotations.md`.
- `pod_path` - pod path for dendron import. Should not need to change. Will likely remove from configuration later so it doesn't get accidentally changed.
- `zotero comment title` - IGNORE FOR NOW. Eventually needed for 2-way sync.

## Import Structure

When a paper is uploaded it will look something like this in your dendron graph.

![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/README.md.Import-paper-graph.png)

Comments notes are synced back to zotero after running `zendron`. They are stored in a file called `zendron_comments` in the note data. After removing all data and running `zendron` again the comments created previously in a local workspace should be imported again. This allows for comments to be easily ported accross projects that reference the same papers.

Comments notes are intended to be used for reference to any annotations under a Zotero item's metadata. This will preserve dendron linking with two-way sync.

## Supplementary import

We support import of supplementary pdfs if they have any of the following prefixes in their pdf title. This can be easily edited within Zotero. We can move this to configuration if custom naming is desired.

```python
["supp",
"Supp",
"supplementary",
"supp.",
"supplementary-material",
"supplementary-materials",
"sup",
"SI",
"si",]
```

## Miscellaneous

- The `zendron_cache` is used for remove of `<user.bibtex_key>.md`. If it is deleted and you run remove, the `<user.bibtex_key>.md` will not be removed. In this case you can run `zendron` again, then run the `zendron remove=true` again.
- If there are run that fail, sometimes a `.hydra` with the given configuraiton will be generated in the root dir. This isn't an issue but it contains the API information and should therefore be added to the `.gitignore` as a safeguard. In addition these files can be used to inspect the reason for the faiure.
- `__main__.log` is generated after running a `zendron`, this can also be deleted as you please. It is also useful for inspecting an failures to import.

## Issues, Troubleshooting, Pull Requests

- If you are having trouble with startup you can use this [Zendron-Test](https://github.com/Mjvolk3/Zendron-Test) template and try to reproduce your issues here. Simply click on `Use this template`, clone the repo and try to run `zendron` here. This will allow for us to catch things we overlooked for different user workspace configuration etc. Once you have tried to reproduce issues here please submit an issue on [Zendron](https://github.com/Mjvolk3/Zendron) linking to your minimal example.

## Common Errors

A list of common errors and quick fixes to address them.

### Error - DendronError: vault with name your-vault-name not found

```bash
DendronError: vault with name <your-vault-name> not found
```

### Fix - DendronError: vault with name your-vault-name not found

This indicates that the vault name in `dendron.yml` was not set.

For example,

```yaml
workspace:
  vaults:
    -
      fsPath: .
      selfContained: true
      name: Zendron
```

### Error - You see a Dendron Pod in your Workspace

- Dendron Pod
  - A Dendron Pod is used for import according to `pod_path` in the `config.yaml`. This dir structure is normally deleted to allow for future importing. If you see it, something is wrong. Create an issue on GitHub, or delete the dir and retry the steps above.

### Fix - You see a Dendron Pod in your Workspace

Delete the pod and rerun zendron to complete. If there is an additional error please report it.
