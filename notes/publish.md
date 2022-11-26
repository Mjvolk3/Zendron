---
id: k0qo53e6jvew0mcyv49bu0e
title: Publish
desc: ''
updated: 1661970817297
created: 1661540036400
---

## To Compile Document
- Run `compile_paper.sh`
    - This currently is slightly broken  due to `./` prepend path issue with pandoc[Pod V2 export asset paths](https://github.com/dendronhq/dendron/issues/3460)
    - **Key** as long as all paths of note assets have `./` prepended the output should be proper.

## Export Markdown Pod
- Configure markdown pod through command palette
- Export pod to folder pod_export

## Pandoc
From root directory run:

```{bash}
pandoc -f gfm --toc -s pod_export/Parameter_Estimation/Paper.md -o paper.docx --reference-doc=reference.docx
```
- `-f` format GitHub ... something style
    - [ ] Look up later
- `--toc` - table of contents
- `-s` - standalone
- `-o` - output
- `--reference-doc` - reference for word formatting. Change this docs formatting to change the export formatting.
- **Note**: Can also use this to export to word

## Resources
- [config.export info](https://wiki.dendron.so/notes/Un0n1ql7LfvMtmA9JEi4n/)