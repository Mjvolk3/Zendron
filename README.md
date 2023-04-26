# Zendron

Version: 1.0.11

## Introduction

- This package was developed for porting Zotero annotations and metadata to markdown. These markdown notes are then brought into a [Dendron](https://www.dendron.so/) hierarchy for integration with vault notes. We recommend using the package within [Visual Studio Code](https://code.visualstudio.com/).The end goal is to get a two way sync between notes in Zotero and notes in Dendron, but this has some difficulties and limitations that are taking some time to address. For now only a one way sync from Zotero to Dendron is supported.

## Install Instructions

- It is recommended to build a [conda env](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for installation.
- Install [Dendron CLI](https://wiki.dendron.so/notes/RjBkTbGuKCXJNuE4dyV6G/).
  - `npm install -g @dendronhq/dendron-cli@latest`
- Install the zendron
  - `python -m pip install zendron`

## Zotero and File Import Configuration

All zendron configuration is handled in [config.yml](https://github.com/Mjvolk3/Zendron/blob/main/conf/config.yaml).

```yml
library_id : 4932032 # Zotero library ID
library_type : group # [user, group] library
api_key : FoCauOvWMlNdYmpYuY5JplTw # Zotero API key
collection: null # Name of Zotero Collection, null for entire library
item_types: [journalArticle, book, preprint, conferencePaper, report] # List of item types according to [pyzotero](https://pyzotero.readthedocs.io/en/latest/)
local_image_path: /Users/<username>/Zotero/cache # Local path for importing annotated images
dendron_limb: zendron.import # Dendron import limb e.g. zendron.import.paper-title.annotations.md
zotero_comment_title: zendron comment # fixed for now... needed for eventual 2-way sync.
pod_path: zotero_pod # Name of dendron pod, removed
```

## Basic Usage

There are only two basic commands that work as of now.

- `zendron`
  - This command imports notes according to a defined [config.yml](https://github.com/Mjvolk3/Zendron/blob/main/conf/config.yaml). Once the command is run the first time the user needs to modify there configuration `./conf/config.yaml` according the zotero library they want to import.
  - Notes are imported with a `## Time Created` heading. This allows for stable reference from other notes, within the note vault. We autogenerate a `*.comments.md` that should be used for taking any additional notes within Dendron. Addition notes taken within the meta data file (`notes/zendron.import.<paper-title>.md`), or the `*.annotations.md` will be overwritten after running `zendron` for a second time.
- `zendron remove=true`
  - This command removes all imported notes and associated links. We run a `createMissingLinkedNotes` following the deletion of Dendron notes to repopulate `tags` and `users` that will be removed on running `zendron-remove`.
  - There are more complicated removal's that could be desired so we plan to eventually change this from a `bool` to `str`.
