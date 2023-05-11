<p align="center">
  <img src="https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/drawio/logo.drawio.png" />
</p>

[![PyPI version](https://badge.fury.io/py/zendron.svg)](https://badge.fury.io/py/zendron)

## Showcase

![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/videos/gif/zendron-test_2.gif)

1. Show how you can structure a paper using note refernces in Dendron.
2. Install Zendron and import references from the relevant library.
3. Cite while you write, and view all relevant Zotero metadata, annotations, and comment notes with hover.
4. Compile paper to `.docx`, `.pdf`, and `.html` with Pandoc.
5. Find relevant papers via VsCode search.

## Introduction

- This package was developed for porting Zotero annotations and metadata to markdown. These markdown notes are then brought into a [Dendron](https://www.dendron.so/) hierarchy for integration with vault notes. We recommend using the package within [Visual Studio Code](https://code.visualstudio.com/).The end goal is to get a two way sync between notes in Zotero and notes in Dendron, but this has some difficulties and limitations that are taking some time to address. For now only a one way sync from Zotero to Dendron is supported.

## Install Instructions

- It is recommended to build a [conda env](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for installation.
- Install [Dendron CLI](https://wiki.dendron.so/notes/RjBkTbGuKCXJNuE4dyV6G/).
  - `npm install -g @dendronhq/dendron-cli@latest`
- Install the zendron
  - `python -m pip install zendron`

## Zotero Local Setup

- To start you need [Better BibTeX for Zotero](https://retorque.re/zotero-better-bibtex/installation/)
  - This allows pinning of of bibtex keys.v
- Go to `Zotero > Settings... > Advanced > General > Config Editor`![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.zotero-config-editor.png)
- Accept the risks ![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.zotero-config-editor-accept-risks.png)
- In the Search, type `autoPinDelay` and chance the integer value from 0 (default) to 1. ![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zendron.citation-key.md.autoPinDelay-update.png)

## Zotero API key

- [Zotero API key](https://www.zotero.org/settings/keys)
- We recommend setting up you Zotero API key with the following settings to allow for full functionality.
  - Personal Library
    - [x] Allow library access.
    - [x] Allow notes access.
    - [x] Allow write access.
  - Default Gropu Permissions
    - [x] Read/Write

![](https://github.com/Mjvolk3/Zendron/raw/main/notes/assets/images/zotero.api-key.md.zotero-api-key.png)

- This key can then be copy pasted in the configuration file. You should add your key to `.gitignore` to prevent others from accessing your Zotoero database. If the key is lost you can always generate a new one.

## Zotero and File Import Configuration

All zendron configuration is handled in [config.yml](https://github.com/Mjvolk3/Zendron/raw/main/conf/config.yaml).

```yml
library_id : 4932032 # Zotero library ID
library_type : group # [user, group] library
api_key : FoCauOvWMlNdYmpYuY5JplTw # Zotero API key
collection: null # Name of Zotero Collection, null for entire library
item_types: [journalArticle, book, preprint, conferencePaper, report] # List of item types according to [pyzotero](https://pyzotero.readthedocs.io/en/latest/)
local_image_path: /Users/<username>/Zotero/cache # Local path for importing annotated images
dendron_limb: zendron.import # Dendron import limb e.g. zendron.import.paper-title.annotations.md
zotero_comment_title: zendron comment # fixed for now... needed for eventual 2-way sync.
pod_path: zotero_pod # Name of dendron pod, removed after completion of import. We will later add configuration for this to remain. This will allow for non Dendron users to import markdown Zotero notes in a strucutred hierarchy.
```

- `library_id` - Integer identifier of library. This is the number that matches the name of a library.
  - [User ID](https://www.zotero.org/settings/keys).
  - For group ID visit [Zotero Groups](https://www.zotero.org/groups/), click on your desired group, and copy the id from the URL.
- `library_type`: `group` for group libraries and `user` for user library.
- `api_key`: Use the API Key obtained from [Zotero API KEY](README.md#zotero-api-key).
- `collection`: This can be the name of any collection or subcollection in the specificed library. If there are multiple collections or sub collections with the same name, the import will arbitrarily choose one. To make sure you are importing the desired collection, make sure the name of the collection is unique in the Zotero library.
- `item_types`: Zotero item types to import according to [pyzotero](https://pyzotero.readthedocs.io/en/latest/) syntax.
`local_image_path`: Path to annotated images. `/Users/<username>/Zotero/cache` is the default path on MacOS.
- `dendron_limb`: This is the period deliminated hierarchy prefix to all file imports for Dendron, e.g. `root.zotero.import.<paper_title>.annotations.md`.
- `zotero comment title` - IGNORE FOR NOW. Eventually needed for 2-way sync.
- `pod_path` - IGNORE FOR NOW. Eventually needed for markdown only import, without Dendron integration.

## Basic Usage

There are only two basic commands that work as of now.

- `zendron`
  - This command should only be run in the root directory of the workspace.
  - This command imports notes according to a defined [config.yml](https://github.com/Mjvolk3/Zendron/raw/main/conf/config.yaml). Once the command is run the first time the user needs to modify their configuration `./conf/config.yaml`. All required configs are marked with a comment `# STARTER CONFIG` upon initialization.
  - Notes are imported with a `## Time Created` heading. This allows for stable reference from other notes, within the note vault. We autogenerate a `*.comments.md` that should be used for taking any additional notes within Dendron. Additional notes taken within the meta data file (`notes/zendron.import.<paper-title>.md`), or the `*.annotations.md` will be overwritten after running `zendron` for a second time. All files downstream of import excpet `*.comments.md` should be treated as read only. We have plans to explicitly make them read only soon.
  - Upon import, notes and tags are left as stubs. To create these notes run `> Dendron: Doctor` then `createMissingLinkedNotes`. It is best practice to correc tag warnings before doing this.
- `zendron remove=true`
  - This command removes imported notes and associated links. This command works by remove all notes downstream fo `dendron_limb`, excpet for `comments.md`. There is some difficult removing other files created becuase these are separate from the `dendron_limb`. These files include `user.*.md`, which comes from bibtex keys, and `tags.*.md` which come from metadata and annotation tags. For now, we don't remove tags, but we do remove bibex keys (`<user.bibtex_key>.md`).
  - There are more complicated removal's that could be desired so we plan to eventually change this from a `bool` to an `str`.

## Miscellaneous

- The `zendron_cache` is used for remove of `<user.bibtex_key>.md`. If it is deleted and you run remove, the `<user.bibtex_key>.md` will not be removed. In this case you can run `zendron` again, then run the `zendron remove=true` again.
- If there are run that fail, sometimes a `.hydra` with the given configuraiton will be generated in the root dir. This isn't an issue but it contains the API information and should therefore be added to the `.gitignore` as a safeguard. In addition these files can be used to inspect the reason for the faiure.
- `__main__.log` is generated after running a `zendron`, this can also be deleted as you please. It is also useful for inspecting an failures to import.

## Troubleshooting

- If you are having trouble with startup you can use this [Zendron-Test](https://github.com/Mjvolk3/Zendron-Test) template and try to reproduce your issues here. Simply click on `Use this template`, clone the repo and try to run `zendron` here. This will allow for us to catch things we overlooked for different user workspace configuration etc. Once you have tried to reproduce issues here please submit an issue on [Zendron](https://github.com/Mjvolk3/Zendron).
