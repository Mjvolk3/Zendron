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

from datetime import datetime

def dendron_timestamp_to_iso_format(timestamp_ms: int) -> str:
    """
    Convert a timestamp in milliseconds to an ISO 8601 formatted date string.

    :param timestamp_ms: The timestamp in milliseconds since the epoch.
    :return: A string representing the date and time in ISO 8601 format.
    """
    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000.0
    
    # Convert the timestamp to a datetime object
    date_time = datetime.utcfromtimestamp(timestamp_s)
    
    # Format the datetime object as an ISO 8601 string, including 'Z' to indicate UTC
    return date_time.strftime('%Y-%m-%dT%H:%M:%SZ')

def read_markdown_file(file_path: str) -> str:
    """
    Read the content of a Markdown file into a string.

    :param file_path: The path to the Markdown file.
    :return: The content of the file as a string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def touch(filename: str) -> None:
    """
    Mimics the behavior of the Unix 'touch' command.

    :param filename: The name of the file to touch.
    """
    with open(filename, "a"):
        pass


@dataclass
class Comment:
    zot: zotero.Zotero
    attachments: list
    title_dendron: str = None
    dendron_limb: str = None
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
        attachment = self.zot.attachment_both(
            [("zendron_comment", filename)], self.parentItem
        )
        comment_key = attachment["unchanged"][0]["key"]
        os.remove(filename)
        return comment_key

    @property
    def dendron_note_path(self):
        # https://wiki.dendron.so/notes/o4i7a81j778jyh7wql0nacb/
        # for selfContained vaults the dir is always notes.
        vault_dir = "./notes"
        # checked and I don't think lower is necessary but it gives a perfect match for the file title
        note_file_name = self.dendron_limb + "." + self.title_dendron.lower() + ".comments.md"
        _dendron_note_path = osp.join(vault_dir, note_file_name)
        return _dendron_note_path

    @property
    def version(self) -> int:
        if self._version is None:
            self._version = self.zot.item(self.comment_key)["data"]["version"]
        return self._version

    @property
    def parentItem(self) -> str:
        if self._parentItem is None:
            self._parentItem = self.zot.item(self.attachments[0]["key"])["data"][
                "parentItem"
            ]
        return self._parentItem

    @property
    def note(self) -> str:
        if self._note is None:
            try:
                self._note = self.get_workspace_comment()
            except AttributeError:
                self._note = ""
        return self._note

    def get_workspace_comment(self):
        md_notes = read_markdown_file(self.dendron_note_path)
        return md_notes
    
    @property
    def dendron_updated_time(self):
        time = front.get_updated_time(self.dendron_note_path)
        _dendron_update_time = dendron_timestamp_to_iso_format(time)
        return _dendron_update_time

def push_comment(zot, comment:Comment):
    item = zot.item(comment.comment_key)
    item["data"]["note"] = comment.note
    zot.update_item(item, comment.version)

class CommentCompiler:
    def __init__(
        self,
        comment: Comment = None,
    ):
        self.comment = comment
        self.title_dendron = comment.title_dendron
        self.dendron_limb = comment.dendron_limb
        self.project_dir: str = os.getcwd().split("/")[-1]
        self.line: str = None

    def compile(self):
        self.line = self.comment.note
        return self.line

    def write_comment(self, pod_path: str = "zendron_pod"):
        path = [pod_path]
        path.extend(self.dendron_limb.split("."))
        path.append(self.title_dendron)
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        file_path = osp.join(path, "comments.md")
        with open(file_path, "w") as f:
            # f.write(self.line)
            # f.write("\n")
            f.write(self.comment.note)
        front.add_comment_key(self.comment.comment_key, file_path)
        front.add_comment_key(self.comment.version, file_path)
        print()


@hydra.main(
    version_base=None,
    config_path=osp.join(os.getcwd(), "conf/zendron"),
    config_name="config",
)
def main(cfg: DictConfig):
    from zendron.items import get_attachments

    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    dendron_limb = cfg.dendron_limb
    zot = zotero.Zotero(library_id, library_type, api_key)

    title_dendron = "Variational-Graph-Auto-Encoders"
    dendron_limb = cfg.dendron_limb

    attachments = get_attachments(zot, "C95VVC24")

    # The essence.
    comment = Comment(
        zot,
        attachments,
        title_dendron,
        dendron_limb,
    )
    comment_compiler = CommentCompiler(comment)
    comment_compiler.compile(comment)
    comment_compiler.write_comment()
    push_comment(zot,comment)


if __name__ == "__main__":
    main()
