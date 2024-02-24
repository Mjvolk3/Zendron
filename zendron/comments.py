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

def read_markdown_file(file_path: str) -> str:
    """
    Read the content of a Markdown file into a string.

    :param file_path: The path to the Markdown file.
    :return: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def touch(filename: str) -> None:
    """
    Mimics the behavior of the Unix 'touch' command.
    
    :param filename: The name of the file to touch.
    """
    with open(filename, 'a'):
        pass  

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
                    if i["title"] == "zendron_comment"
                ][0]
            except IndexError:
                self._comment_key = self.attach_empty_md()
        return self._comment_key
    
    def attach_empty_md(self):
        filename = "zendron_temp.md"
        touch(filename)
        attachment = self.zot.attachment_both([("zendron_comment", filename)], self.parentItem)
        comment_key = attachment['unchanged'][0]['key']
        os.remove(filename)
        return comment_key

    @property
    def version(self) -> int:
        if self._version is None:
            self._version = self.zot.item(self.comment_key)["data"]["version"]
        return self._version

    @property
    def parentItem(self) -> str:
        if self._parentItem is None:
            self._parentItem = self.zot.item(self.attachments[0]['key'])['data']['parentItem']
        return self._parentItem

    @property
    def note(self) -> str:
        if self._note is None:
            try:
                self.get_workspace_comment()
                self._note = self.zot.item(self.comment_key)["data"]["note"]
            except AttributeError:
                self._note = ""
        return self._note

    def get_workspace_comment(self):
        print()
        pass


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

    def write_comment(self, pod_path: str = "zendron_pod"):
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
        front.add_comment_key(self.comment.version, file_path)


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf/zendron"), config_name="config"
)
def main(cfg: DictConfig):
    from zendron.items import get_attachments
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    dendron_limb = cfg.dendron_limb
    zot = zotero.Zotero(library_id, library_type, api_key)
    
    attachments = get_attachments(zot, "C95VVC24")
    comment = Comment(zot, attachments)
    comment.comment_key
    ####
    comment_compiler = CommentCompiler(
        comment, 'Variational-Graph-Auto-Encoders', cfg.dendron_limb
    )
    comment_compiler.compile(comment)
    comment_compiler.write_comment()
    # comment.version    
    print()
    
    #TODO you need this!! 
    
    #(".").join(file_path.split(".md")[0].split("/")[1:])

if __name__ == "__main__":
    main()
