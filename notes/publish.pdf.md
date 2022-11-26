---
id: p6evbyfciaotkrkwav3ipra
title: Pdf
desc: ''
updated: 1661893252368
created: 1661892034192
---

## Merge Tools
- [PDF Merge Tools](https://sites.astro.caltech.edu/observatories/coo/solicit/mergePDF.html#:~:text=ghostscript%20is%20commonly%2Ftypically%20foun

### Linux and MacOS
- Ghostscript (`gs`) is often natively installed
- ```
    gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=combined.pdf -dBATCH pdf1.pdf pdf2.pdf pdf3.pdf ...
    ```
### Windows
- Have not tested but it looks relatively easy to use.
- [pdftk download](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/)
- [pdftk examples](https://www.pdflabs.com/docs/pdftk-cli-examples/)
- `pdftk in1.pdf in2.pdf cat output out1.pdf`
