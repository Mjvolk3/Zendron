import json
import logging
import os
import os.path as osp
import shutil
from dataclasses import dataclass, field
from datetime import datetime

from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron.date import utc_parse

log = logging.getLogger(__name__)


@dataclass
class Annotation:
    annotation: dict = None
    local_image_path: str = None
    name: str = field(init=False, repr=False)

    def __post_init__(self):
        self.name: str = self.annotation["library"]["name"]

    def get_color(self):
        color = self.annotation["data"]["annotationColor"]
        color_emoji = ""
        if color == "#5fb236":
            color_emoji = "🟢 "
        elif color == "#2ea8e5":
            color_emoji = "🔵 "
        elif color == "#a28ae5":
            color_emoji = "🟣 "
        elif color == "#ff6666":
            color_emoji = "🔴 "
        elif color == "#ffd400":
            color_emoji = "🟡 "
        else:
            color_emoji = "❓ "
        return color_emoji

    def get_annotation_text(self):
        try:
            annotation_text = self.annotation["data"]["annotationText"]
        except KeyError:
            annotation_text = ""
        return annotation_text

    def get_annotation_author_name(self):
        try:
            annotation_author_name = self.annotation["meta"]["createdByUser"][
                "username"
            ]
            # previously works for user libraries
            # annotation_author_name = self.annotation["data"]["annotationAuthorName"]
            # TODO need to test if this works in user libraries
        except KeyError:
            annotation_author_name = "Unknown"
        return annotation_author_name

    def get_annotation_comment(self):
        annotation_comment = self.annotation["data"]["annotationComment"]
        return annotation_comment

    def format_annotation_comment(
        self,
        lines: list = None,
        annotation_comment: str = "",
        color_emoji: str = "",
        color_emoji_cfg: bool = True,
    ):
        if annotation_comment != "":
            if color_emoji_cfg is True:
                color_indicator = f"({color_emoji}) "
            else:
                color_indicator = ""
            lines.append(f"- Comment {color_indicator}: {annotation_comment}")
        else:
            if color_emoji_cfg is True:
                color_indicator = f"({color_emoji}) "
            else:
                color_indicator = ""
            # For some reason there is an extra space added. Reason for [:-1].
            lines.append(f"- Comment {color_indicator}"[:-1])

        return lines

    def get_annotation_tags(self):
        annotation_tags = ", ".join(
            [f"#{i['tag']}" for i in self.annotation["data"]["tags"]]
        )
        return annotation_tags

    def format_annotation_tags(self, lines: list, annotation_tags: str):
        cfg_annotations_tags_format = True

        if annotation_tags != "":
            if " " in lines:
                log.warning(
                    f"Tags should not contain spaces. Please remove spaces in Zotero annotations and sync again. Tag: {annotation_tags}"
                )
            if cfg_annotations_tags_format:
                lines.append(f"- Tags: {annotation_tags}")
        return lines

    def format_annotation_text(self, lines: list, annotation_text: str):
        if annotation_text == "":
            return lines
        lines.append(f"\n> {annotation_text}")
        return lines

    def get_annotation_link(self):
        pass

    def get_date_added(self):
        date_added = utc_parse(self.annotation["data"]["dateAdded"])
        return date_added

    def get_image(self):
        # HACK for images
        if self.annotation["data"]["annotationType"] != "image":
            return None
        image_id = self.annotation["data"]["key"]
        if self.annotation["library"]["type"] == "user":
            image_src = f"library/{image_id}.png"
        elif self.annotation["library"]["type"] == "group":
            image_src = f"groups/{self.annotation['library']['id']}/{image_id}.png"
        image_src = osp.join(self.local_image_path, image_src)
        image_dest = f"notes/assets/images/zendron-image-import-{image_id}.png"
        shutil.copyfile(image_src, image_dest)
        image_link = f"![](./{'/'.join(image_dest.split('/')[1:])})"
        return image_link


# TODO Should really take metadata as an argument. Specifically for user_path
class AnnotationsCompiler:
    def __init__(
        self,
        annotation_title: str = None,
        title_dendron: str = None,
        local_image_path: str = None,
        dendron_limb: str = None,
        pod_path: str = None,
    ):
        self.annotation_title = annotation_title
        self.title_dendron = title_dendron
        self.local_image_path = local_image_path
        self.dendron_limb: str = dendron_limb
        self.pod_path: str = pod_path
        self.project_dir: str = os.getcwd().split("/")[-1]
        self.lines: list = None

    def get_local_annotation_link(self):
        local_annotations_link = f"dendron://{self.project_dir}/{self.dendron_limb}.{self.title_dendron}.comments"
        local_annotations_link_wiki = f"[[Local Comments|{local_annotations_link}]]"
        return local_annotations_link_wiki

    # TODO check if annotations are list[dict]
    def compile(self, annotations: list = None) -> list:
        lines = []
        lines.append("## Annotations")
        # save annotations to txt file
        # TODO default sort order is ['data']['dateModified']. Add config to allow for
        for i, annot in enumerate(annotations):
            annot = Annotation(annot, self.local_image_path)
            # TODO separate out all of these into their own functions
            # annotation_keys.append(i['key'])
            # lines.append(annot['data']['annotationPageLabel'])
            date_added = annot.get_date_added()
            lines.append(f"\n### Date Added: {date_added}")
            annotation_text = annot.get_annotation_text()
            lines = annot.format_annotation_text(lines, annotation_text)
            lines.append("")
            image_link = annot.get_image()
            if image_link is not None:
                lines.append(f"{image_link}\n")
            lines.append(f"- Annotator: @{annot.get_annotation_author_name()}")
            color_emoji = annot.get_color()
            annotation_comment = annot.get_annotation_comment()
            lines = annot.format_annotation_comment(
                lines, annotation_comment, color_emoji, color_emoji_cfg=True
            )
            tags = annot.get_annotation_tags()
            lines = annot.format_annotation_tags(lines, tags)
        lines.append("\n## Local Comments\n")
        lines.append(f"- {self.get_local_annotation_link()}")
        self.lines = lines
        return lines

    def write(self):
        path = [self.pod_path]
        path.extend(self.dendron_limb.split("."))
        path.append(self.title_dendron)
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        with open(osp.join(path, f"{self.annotation_title}.md"), "w") as f:
            for line in self.lines:
                f.write(line)
                f.write("\n")


def main():
    pass


if __name__ == "__main__":
    main()
