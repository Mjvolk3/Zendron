#!/usr/bin/env bash
eval "$(conda shell.bash hook)"
conda activate zendron
# TODO find a better option than clearing previous... cache should fix this.
# removes all import notes... preserves local note ref
echo "Removing all Zendron Note Files"
rm -r notes/zendron.import.*.md
# removes all user and tags that would have been metioned in notes
rm -r notes/user.*.md
rm -r notes/tags.*.md
echo "Removing all Zendron Cache"
rm zendron_cache/metadata_cache.json
rm zendron_cache/annotations_cache.json
# recreates missing links for delete `user and tags that could be used by other notes other than zendron.import limb.
echo "Creating Missing Linked Notes"
dendron doctor --action createMissingLinkedNotes
