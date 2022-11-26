#!/usr/bin/env bash
eval "$(conda shell.bash hook)"
conda activate zendron
# TODO find a better option than clearing previous... cache should fix this.
#echo "Removing zendron.import.*.md"
#rm -r notes/zendron.import.*.md
python src/zendron/resync.py
dendron importPod --podId dendron.markdown --wsRoot .
# don't need to see pod and should remove everytime
rm -r zotero_pod
echo "Sync Complete"
