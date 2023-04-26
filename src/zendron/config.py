from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore


@dataclass
class ZendronConfig:
    library_id : 4932032 #9025336 my user
    library_type : group
    api_key : FoCeuOvWMnNdYmpYuY5JpETw
    collection: null # null if not specified.
    item_types: [journalArticle, book, preprint, conferencePaper, report]
    local_image_path: /Users/michaelvolk/Zotero/cache
    dendron_limb: zendron.import
    zotero_comment_title: zendron comment
    pod_path: zotero_pod

def main():
    pass


if __name__ == "__main__":
    main()
