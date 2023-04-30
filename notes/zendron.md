---
id: 3bgot52d1psalztauw89ii9
title: Zendron
desc: ''
updated: 1674699629068
created: 1669323977999
---
## Basics

### Zotero BibTex Setup

- Right click on your library and select **Export Library...**

![](/assets/images/Zotero-automatic-export-library.png)

- Make sure the Format is **Better BibTeX**, check **Keep updated** and **Background export**, then select **OK**.

![](/assets/images/Zotero-automatic-export-library-options.png)

- Save as `notes/bib/bib.bib`. This is the default that currently works with zendron.

![](/assets/images/Zotero-automatic-export-library-dir.png)

- **Note**: Sometimes there are issues with the automatic export. See [[Known Issues|zendron#known-issues]].

### Command Palette

- `Tasks: Run Task`
  - `Zendron: Sync`
    - Updates the imported Zotero library based on the cache
    - Use when you make a few annotations in Zotero and you would like to update
  - `Zendron: Resync`
    - Imports the entire Zotero library
    - Use when you are first importing or after running `Zendron: Remove`
  - `Zendron: Remove`
    - Remove dendron limb `Root.Zendron.Import.*`
    - `Root.Zendron.Local.*` is preserved
    - Removes all `Root.Tags.*`, Run `Dendron: Doctor`, `createMissingLinkedNotes` to generate tags from other notes
    - Removes all `Root.User.*`, Run `Dendron: Doctor`, `createMissingLinkedNotes` to generate User from other notes

### Import Structure

All notes created directly with Zendron will be downstream of the `Root.Zendron`.
![](/assets/images/zendron-import-graph-structure.png)

#### Import

These are notes imported directly from Zotero with zendron. **NEVER** modify these notes, any edits you make will be lost on `resync` and `sync`

#### Local

These notes mirror the imported limb, but instead of `Annotations` leaves they have `Comments` leaves. There is a wiki link connecting `Annotations` → `Comments`. Additional comments and discussion of a particular item should exist in `Comments`. `Comments` can be used to reference `Annotations` by using `Dendron: Copy Note Ref` on a **3H** comment heading that contains **Date Added**). You will not see an anchor when you link this way. Your ref should contain something like `#date-added-2022-08-29-2152400000,1:#*`. Linking this way preserves connections on running `sync` and `resync`. In the example `Dendron: Copy Note Ref` is used on an annotation so we get the bidirectional link you see.

![](/assets/images/zendron-import-local-link.png)

### Using With Dendron

- After import you can run `Dendron: Doctor`, `createMissingLinkedNotes` to get all links
- You can also use `Dendron: Doctor`, `removeStubs`to remove some of these unwanted notes. **Note** This will remove other notes that don't contain any content.
- If the `Dendron: Show Note Graph` looks like it is showing redundant information, close the window, run `Dendron: Reindx`, and run `Dendron: Show Note Graph` again.

## Known Issues

- If there is a `cite_key` error the BibTex bibliography is probably out of date. Refresh the export by first going to **Preferences** in **Zotero**.

![](/assets/images/Zotero-preferences.png)

- Go to **Better BibTeX** and then select tab **Automatic export**.

![](/assets/images/Zotero-preference-automatic-export.png)

- Select **Export now**.
