import json
import logging
import os
import os.path as osp
from dataclasses import dataclass, field
from datetime import datetime

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron.annotations import AnnotationsCompiler
from zendron.comments import Comment, CommentCompiler
from zendron.items import get_annotated_attachments, get_attachments, get_metadatas
from zendron.metadata import Metadata, MetadataCompiler

log = logging.getLogger(__name__)


@dataclass
class UserCitationKey:
    metadata: Metadata
    pod_path: str
    _metadata_wiki: str = None
    _comments_wiki: str = None
    _annotations_wiki: str = None

    @property
    def metadata_wiki(self):
        if self._metadata_wiki is None:
            alias = "metadata"
            link = f"dendron://{self.metadata.project_dir}/{self.metadata.dendron_limb}.{self.metadata.title_dendron}"
            self._metadata_wiki = f"[[{alias}|{link}]]"
        return self._metadata_wiki

    @property
    def comments_wiki(self):
        if self._comments_wiki is None:
            alias = "comments"
            link = f"dendron://{self.metadata.project_dir}/{self.metadata.dendron_limb}.{self.metadata.title_dendron}.comments"
            self._metadata_wiki = f"[[{alias}|{link}]]"
        return self._metadata_wiki

    @property
    def annotations_wiki(self):
        if self._annotations_wiki is None:
            alias = "annotations"
            link = f"dendron://{self.metadata.project_dir}/{self.metadata.dendron_limb}.{self.metadata.title_dendron}.annotations"
            self._metadata_wiki = f"[[{alias}|{link}]]"
        return self._metadata_wiki

    # only currently support one attachment which is annotations. Need to refactor metadata adding properties for the methods, or initializing in post_init.


class UserCitationKeyCompiler:
    def __init__(self, user_citation_key: UserCitationKey):
        self.user_citation_key = user_citation_key
        self.metadata = user_citation_key.metadata
        self.pod_path = user_citation_key.pod_path
        self.lines: list = None

    def compile(self) -> str:
        lines = []
        lines.append("## Metadata\n\n***\n")
        lines.append(f"{self.user_citation_key.metadata_wiki}")
        lines.append(f"!{self.user_citation_key.metadata_wiki}")
        lines.append("\n***\n")
        lines.append("## Comments\n\n***\n")
        lines.append(f"{self.user_citation_key.comments_wiki}")
        lines.append(f"!{self.user_citation_key.comments_wiki}")
        lines.append("\n***\n")
        lines.append("## Annotations\n\n***\n")
        lines.append(f"{self.user_citation_key.annotations_wiki}")
        lines.append(f"!{self.user_citation_key.annotations_wiki}")
        lines.append("\n***")
        self.lines = lines
        return lines

    def write(self):
        path = osp.join(self.pod_path, "user")
        os.makedirs(path, exist_ok=True)
        file_path = osp.join(path, f"{self.metadata.citation_key}.md")
        with open(file_path, "w") as f:
            for line in self.lines:
                f.write(line)
                f.write("\n")


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf"), config_name="config"
)
def main(cfg: DictConfig):
    pass


if __name__ == "__main__":
    main()
