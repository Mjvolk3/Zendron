# %%
import glob
import json
import logging
import os
import os.path as osp
from dataclasses import dataclass, field
from datetime import datetime

import frontmatter
import hydra
from html2text import html2text
from hydra import compose, initialize
from markdown import markdown
from markdownify import markdownify as md
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron import front
from zendron.annotations import AnnotationsCompiler
from zendron.metadata import Metadata, MetadataCompiler


@dataclass
class Comment:
    zot: zotero.Zotero
    attachments: list
    _note: str = None
    _comment_key: str = None
    _version: int = None
    _parentItem: str = None

    @property
    def comment_key(self) -> str:
        if self._comment_key is None:
            try:
                self._comment_key = [
                    i["key"]
                    for i in self.attachments
                    if i["zendron_title"] == "zendron comment"
                ][0]
            except IndexError:
                self._comment_key = None
        return self._comment_key

    @property
    def version(self) -> int:
        if self._version is None:
            self._version = self.zot.item(self.comment_key)["data"]["version"]
        return self._version

    @property
    def parentItem(self) -> str:
        if self._parentItem is None:
            try:
                self._parentItem = self.zot.item(self.comment_key)["data"]["parentItem"]
            except AttributeError:
                self._parentItem = ""
        return self._parentItem

    @property
    def note(self) -> str:
        if self._note is None:
            try:
                self._note = self.zot.item(self.comment_key)["data"]["note"]
            except AttributeError:
                self._note = ""
        return self._note


class CommentCompiler:
    def __init__(
        self,
        comment: Comment = None,
        title_dendron: str = None,
        dendron_limb: str = None,
    ):
        self.comment = comment
        self.title_dendron = title_dendron
        self.dendron_limb: str = dendron_limb
        self.project_dir: str = os.getcwd().split("/")[-1]
        self.line: str = None

    def compile(self, comment: Comment = None):
        self.line = comment.note
        return self.line

    def write_comment(self, pod_path: str = "zotero_pod"):
        path = [pod_path]
        path.extend(self.dendron_limb.split("."))
        path.append(self.title_dendron)
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        file_path = osp.join(path, "comments.md")
        with open(file_path, "w") as f:
            f.write(self.line)
            f.write("\n")
        front.add_comment_key(self.comment.comment_key, file_path)


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf"), config_name="config"
)
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    dendron_limb = cfg.dendron_limb
    zot = zotero.Zotero(library_id, library_type, api_key)

    # comment = Comment()
    # comment_compiler = CommentCompiler()
    # comment_compiler.compile()
    # comment_compiler.write_comment()


if __name__ == "__main__":
    main()
