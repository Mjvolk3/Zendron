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

# @dataclass
# class Comment:
#     zot: zotero.Zotero = None
#     dendron_limb: str = None
#     zotero_comment_title: str = None
#     _formatted_title: str = None

#     @property
#     def format_zotero_comment_title(self) -> str:
#         if self._formatted_title is None:
#             self._formatted_title = f"{self.zotero_comment_title}\n"
#         return self._formatted_title

#     def title_check(self, note: str = None) -> str:
#         zotero_title = self.format_zotero_comment_title(self.zotero_comment_title)
#         extracted_title = note[: len(zotero_title)]
#         return zotero_title == extracted_title


# def load_comment():
#     comment_paths = glob.glob(osp.join("notes", f"{dendron_limb}.*.comments.md"))
#     leaf_paths = glob.glob(osp.join("notes", f"{dendron_limb}.*.*.md"))
#     possible_paths = glob.glob(osp.join("notes", f"{dendron_limb}.*.md"))
#     meta_paths = list(set(possible_paths) - set(leaf_paths))
#     for path in meta_paths:
#         child = zotero_comment(path, zot, self.zotero_comment_title)
#         if child is not None:
#             note = child["data"]["note"]
#             comment_title = format_zotero_comment_title(self.zotero_comment_title)
#             zotero_note = last_note[len(comment_title) :]
#     return last_note


# def zotero_comment(
#     meta_path: str,
#     zot: zotero.Zotero = None,
#     zotero_comment_title: str = None,
# ) -> dict:
#     data = frontmatter.load(meta_path)
#     children = zot.children(data["metadata_key"])
#     for child in children:
#         if child["data"]["itemType"] == "note" and title_check(
#             zotero_comment_title, child["data"]["note"]
#         ):
#             return child
#     return None


# def format_zotero_comment_title(zotero_comment_title) -> str:
#     formatted_title = f"{zotero_comment_title}\n"
#     return formatted_title


# def sync_comments(
#     zot: zotero.Zotero = None,
#     dendron_limb: str = None,
#     zotero_comment_title: str = None,
# ):
#     paths = glob.glob(osp.join("notes", f"{dendron_limb}.*.comments.md"))
#     for path in paths:
#         meta_note_path = (path.split(".")[:-2]) + ["md"]
#         meta_note_path = ".".join(meta_note_path)
#         data = frontmatter.load(meta_note_path)

#         with open(path, "r") as f:
#             text = f.read()
#             text = format_zotero_comment_title(zotero_comment_title) + text
#         note = zot.item_template("note")
#         # No conversion to HTML for easy Zotero reading.
#         note["note"] = text
#         comment = zotero_comment(zot, dendron_limb, zotero_comment_title)
#         if comment is not None and comment["data"]["note"] != text:
#             comment["note"] = text
#             zot.update_item(comment)
#         else:
#             zot.create_items([note], data["metadata_key"])


# def to_file(markdown):
#     with open("delete.md", "w") as f:
#         f.write(markdown)


@hydra.main(
    version_base=None, config_path=osp.join(os.getcwd(), "conf"), config_name="config"
)
def main(cfg: DictConfig):
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    dendron_limb = cfg.dendron_limb
    zot = zotero.Zotero(library_id, library_type, api_key)
    raw_text = sync_comments(
        zot, dendron_limb, zotero_comment_title=cfg.zotero_comment_title
    )
    text = read_comments(zot, dendron_limb)
    to_file(text)

    # comment = Comment()
    # comment_compiler = CommentCompiler()
    # comment_compiler.compile()
    # comment_compiler.write_comment()


if __name__ == "__main__":
    main()
