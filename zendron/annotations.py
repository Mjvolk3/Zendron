# zendron/annotations
# [[Zzendron.annotations]]
# https://github.com/Mjvolk3/Zendron/tree/main/zendron/annotations
# Test file: tests/zendron/test_annotations.py

import json
import logging
import os
import os.path as osp
import shutil
from dataclasses import dataclass, field
from datetime import datetime
import subprocess
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
    _image_src_path: str = field(init=False, repr=False)

    def __post_init__(self):
        self.name: str = self.annotation["library"]["name"]

    def get_color(self):
        color = self.annotation["data"]["annotationColor"]
        color_emoji = ""
        if color == "#5fb236":
            color_emoji = "🟢"
        elif color == "#2ea8e5":
            color_emoji = "🔵"
        elif color == "#a28ae5":
            color_emoji = "🟣"
        elif color == "#ff6666":
            color_emoji = "🔴"
        elif color == "#ffd400":
            color_emoji = "🟡"
        elif color == "#f19837":
            color_emoji = "🟠"
        elif color == "#aaaaaa":
            color_emoji = ""
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
            if self.annotation["library"]["type"] == "user":
                annotation_author_name = self.annotation['library']['name']
            else:
                annotation_author_name = self.annotation["meta"]["createdByUser"][
                    "username"
                ]
        except KeyError:
            annotation_author_name = "unknown"
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
        annotation_tags = [i["tag"] for i in self.annotation["data"]["tags"]]
        return annotation_tags

    def format_annotation_tags(self, lines: list, annotation_tags: str):
        if annotation_tags != "":
            if " " in lines:
                log.warning(
                    f"Tags should not contain spaces. Please remove spaces in Zotero annotations and sync again. Tag: {annotation_tags}"
                )
            else:
                readable_annotation_tags = ", ".join(
                    [f"#{i}" for i in self.get_annotation_tags()]
                )
                lines.append(f"- Tags: {readable_annotation_tags}")
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

    @property
    def image_src_path(self):
        if self.annotation["data"]["annotationType"] != "image":
            return None
        image_id = self.annotation["data"]["key"]
        if self.annotation["library"]["type"] == "user":
            image_src = f"library/{image_id}.png"
        elif self.annotation["library"]["type"] == "group":
            image_src = f"groups/{self.annotation['library']['id']}/{image_id}.png"
        self._image_src_path = osp.join(self.local_image_path, image_src)
        return self._image_src_path

    def get_image_dest_path(self):
        if self.annotation["data"]["annotationType"] != "image":
            return None
        image_id = self.annotation["data"]["key"]
        image_dest = f"notes/assets/images/zendron-image-import-{image_id}.png"
        return image_dest

    def get_image_link(self):
        image_dest = self.get_image_dest_path()
        shutil.copyfile(self.image_src_path, image_dest)
        image_link = f"![](./{'/'.join(image_dest.split('/')[1:])})"
        return image_link

    def mpx_convert_image_to_tex(self) -> str:
        """Converts the annotation image to LaTeX (.tex) format using Mathpix CLI,
        handles the .zip output, and reads the .tex content.
        """
        image_path = self.image_src_path
        if not image_path or not os.path.exists(image_path):
            return ""

        # Define the output ZIP file path as a temporary file in the root directory
        tex_file_path = os.path.join(os.getcwd(), "mpx-zendron-temp.tex")

        # Update the command to output a .zip file (assuming .zip is the default or required format)
        command = f"mpx convert {image_path} {tex_file_path}"

        try:
            # Execute the Mathpix CLI command
            subprocess.run(command, check=True, shell=True)
            tex_output_file_path = tex_file_path + ".zip"
            # Read the .tex content
            with open(tex_output_file_path, "r") as tex_file:
                tex_content = tex_file.read()

            # Delete the temporary .zip file
            os.remove(tex_output_file_path)

            return tex_content
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to convert image to LaTeX: {e}")
        except Exception as e:
            log.error(f"Error during file handling: {e}")

        return ""

    def format_mpx_equation(self, equation: str) -> str:
        """Formats a LaTeX equation by removing '\\[' and '\\]' delimiters and wrapping it with '$$' for Markdown."""
        # Trim the starting '\\[' and ending '\\]' if they exist
        trimmed_equation = equation.strip()
        if trimmed_equation.startswith("\\["):
            trimmed_equation = trimmed_equation[2:]
        if trimmed_equation.endswith("\\]"):
            trimmed_equation = trimmed_equation[:-2]

        # Trim any leading or trailing whitespace again after removing delimiters
        trimmed_equation = trimmed_equation.strip()

        # Wrap the equation with '$$' for Markdown
        return f"$$\n{trimmed_equation}\n$$\n"


# TODO Should really take metadata as an argument. Specifically for user_path
class AnnotationsCompiler:
    def __init__(
        self,
        annotation_title: str = None,
        title_dendron: str = None,
        local_image_path: str = None,
        dendron_limb: str = None,
        pod_path: str = None,
        mathpix: bool = True,
    ):
        self.annotation_title = annotation_title
        self.title_dendron = title_dendron
        self.local_image_path = local_image_path
        self.dendron_limb = dendron_limb
        self.pod_path = pod_path
        self.project_dir = os.getcwd().split("/")[-1]
        self.lines: list = None
        self.mathpix: bool = mathpix

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
        sorted_annotations = sorted(
            annotations, key=lambda x: x["data"]["annotationSortIndex"]
        )
        for i, annot in enumerate(sorted_annotations):
            annot = Annotation(annot, self.local_image_path)
            # TODO separate out all of these into their own functions
            # annotation_keys.append(i['key'])
            # lines.append(annot['data']['annotationPageLabel'])
            date_added = annot.get_date_added()
            lines.append(f"\n### Date Added: {date_added}")
            annotation_text = annot.get_annotation_text()
            lines = annot.format_annotation_text(lines, annotation_text)
            lines.append("")
            image_dest_path = annot.get_image_dest_path()
            tags = annot.get_annotation_tags()
            # Convert both lists to sets
            # Check if there is any intersection between the two sets
            if image_dest_path is not None and self.mathpix and "mpx" in tags:

                # mathpix logic on the path to the png.
                line = annot.mpx_convert_image_to_tex()
                line = annot.format_mpx_equation(line)
                lines.append(line)
            elif image_dest_path is not None:
                lines.append(f"{annot.get_image_link()}\n")

            lines.append(f"- Annotator: @{annot.get_annotation_author_name()}")
            color_emoji = annot.get_color()
            annotation_comment = annot.get_annotation_comment()
            lines = annot.format_annotation_comment(
                lines, annotation_comment, color_emoji, color_emoji_cfg=True
            )
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
