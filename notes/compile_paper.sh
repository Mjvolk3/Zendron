#!/usr/bin/env bash
# Activate env
eval "$(conda shell.bash hook)"
conda activate zendron
# TODO check if it should be at root?
# Export Dendron vault to markdown that can be compiled into document
# Create Bubble Graph - This should be moved into github actions
dendron visualize --out assets

# export pod
dendron exportPodV2 --podId paper --fname paper --vault Parameter_Estimation

# Find a and replace asset paths. Prepend `./` to 'assets' so they can be recognized by Pandoc
echo 'Correcting paths for Pandoc'
sed -i '' 's/](assets/](.\/assets/g' *.md

# Pandoc to construct documents
# table of contents option
# pandoc -f gfm --toc -B pod_export/Parameter_Estimation/paper/title.md pod_export/Parameter_Estimation/Paper.md -o paper.pdf --reference-doc=reference.docx

# For thesis: pandoc -s notes/export/paper.docx notes/export/paper0.docx -o out.docx --reference-doc=notes/ms_word_ref/paper-reference.docx --citeproc --bibliography notes/bib/bib.bib --metadata csl=notes/bib/nature.csl --toc

# docx - If output looks wrong change/modify paper-reference.docx
pandoc -s export/Parameter_Estimation/Paper.md -o export/paper.docx --reference-doc=ms_word_ref/paper-reference.docx --citeproc --bibliography bib/bib.bib --metadata csl=bib/nature.csl

# pdf - If output looks wrong can change PDF engine
pandoc -s export/Parameter_Estimation/Paper.md -o export/paper.pdf --reference-doc=ms_word_ref/paper-reference.docx --citeproc --bibliography bib/bib.bib --metadata csl=bib/nature.csl -V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm" --strip-comments

echo "Paper compiled!"
echo "Find at 'notes/export/paper.docx' and 'notes/export/paper.pdf'"
