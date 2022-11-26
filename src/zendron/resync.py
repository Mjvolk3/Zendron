# %%
import json
import logging
import os
import os.path as osp
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime

import bibtexparser
import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

# set logger
log = logging.getLogger(__name__)
# Globals
global POD_PATH
POD_PATH = "zotero_pod"
global DENDRON_LIMB
DENDRON_LIMB = "zendron.import"
global LIBRARY_TYPE
LIBRARY_TYPE = "group"  # or 'user'
global PROJECT_DIR
PROJECT_DIR = os.getcwd().split("/")[-1]
# %%
def utc_parse(date_string):
    # substitute Z with +00:00 for proper UTC formatting. Z stands for 0 offset.
    if date_string[-1] == "Z":
        date_string = date_string[:-1] + "+00:00"
    return datetime.fromisoformat(date_string)


# TODO fix paths so it can be run from in zendron or in root and still output to notes. Also zotero_pod should be written in zendron so caching can be implemented within the folder. Maybe zendron/data?
@dataclass
class Metadata:
    metadata: dict = None
    bib_path: str = "notes/bib/bib.bib"
    title_dendron: str = field(init=False, repr=False)
    doi: str = field(init=False, repr=False)
    attachment_id: str = field(init=False, repr=False)
    id: str = field(init=False, repr=False)
    key: str = field(init=False, repr=False)
    name: str = field(init=False, repr=False)

    def __post_init__(self):
        self.title_dendron: str = self.get_title_dendron()
        self.id: str = self.metadata["library"]["id"]
        self.key: str = self.metadata["key"]
        self.name: str = self.metadata["library"]["name"]

    def get_title_dendron(self):
        title = self.metadata["data"]["title"]
        title_dendron = "-".join(title.split(" "))
        return title_dendron

    def get_title(self):
        title = self.metadata["data"]["title"]
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.title.{self.title_dendron}"
        title_wiki = f"[[{title}|{link}]]"
        return title_wiki

    def get_creators(self):
        creators = self.metadata["data"]["creators"]
        # creatorType key exists too... think it is always author... or mostly
        creators_wiki = []
        for creator in creators:
            name = []
            first_name = creator["firstName"]
            last_name = creator["lastName"]
            name.extend([first_name, last_name])
            name_alias = " ".join(name)
            name_den = "-".join(name).replace(" ", "-").replace(".", "")
            link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.authors.{name_den}"
            wiki = f"[[{name_alias}|{link}]]"
            creators_wiki.append(wiki)
        creators_wiki = ", ".join(creators_wiki)
        return creators_wiki

    def mdy_to_ymd(self, date):
        month_abbr = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        if (date.split(" ")[0] in month_abbr) and ("," in date.split(" ")[1]):
            # change myd to myd date format
            date = date.split(" ")
            date[1] = date[1].replace(",", "")
            date = "-".join(date)
            date = datetime.strptime(date, "%b-%d-%Y")
            date = date.strftime("%Y-%m-%d")
        return date

    def get_date(self):
        # TODO helper function - same get_access_date
        try:
            date = utc_parse(self.metadata["data"]["date"])
        except ValueError as e:
            date = self.mdy_to_ymd(self.metadata["data"]["date"])
        date = str(date).split(" ")[0]
        date_dendron = date.replace("-", ".")
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.date.{date_dendron}"
        date_wiki = f"[[{date}|{link}]]"
        return date_wiki

    def get_access_date(self):
        try:
            access_date = utc_parse(self.metadata["data"]["accessDate"])
            access_date = str(access_date).split(" ")[0]
            date_dendron = access_date.replace("-", ".")
            link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.date.{date_dendron}"
            access_date_wiki = f"[[{access_date}|{link}]]"
        except:
            access_date_wiki = "No access date"
        return access_date_wiki

    def get_date_added(self):
        # TODO helper function - same ad get_date_modified
        date_added = utc_parse(self.metadata["data"]["dateAdded"])
        date_added = str(date_added).split(" ")
        date_added = "-".join(date_added)
        date_added = date_added.split("+")[:-1]
        date_added = "-".join(date_added)
        date_added = date_added.replace(":", "-")
        date_dendron = date_added.replace("-", ".")
        date_dendron = date_added.replace("-", ".")
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.date.{date_dendron}"
        date_added_wiki = f"[[{date_added}|{link}]]"
        return date_added_wiki

    def get_date_modified(self):
        date_modified = utc_parse(self.metadata["data"]["dateModified"])
        date_modified = str(date_modified).split(" ")
        date_modified = "-".join(date_modified)
        date_modified = date_modified.split("+")[:-1]
        date_modified = "-".join(date_modified)
        date_modified = date_modified.replace(":", "-")
        date_dendron = date_modified.replace("-", ".")
        date_dendron = date_modified.replace("-", ".")
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.date.{date_dendron}"
        date_modified_wiki = f"[[{date_modified}|{link}]]"
        return date_modified_wiki

    def get_url(self):
        url = self.metadata["data"]["url"]
        url = str(f"[{url}]({url})")
        return url

    def get_DOI(self):
        try:
            doi = self.metadata["data"]["DOI"]
            self.doi = doi
            link = f"http://doi.org/{doi}"
            doi = str(f"[{doi}]({link})")
        except KeyError:
            self.doi = "No DOI"
            doi = "No DOI"
        return doi

    def fix_bibtex(self):
        # Handle issue with months
        # TODO check that this doesn't created an error with  pandoc bib render
        bib_fix_path = self.bib_path.replace(".bib", "_fix.bib")
        # copy self.bib_path to fix_path
        shutil.copyfile(self.bib_path, bib_fix_path)
        month_abbreviations = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
        for month in month_abbreviations:
            subprocess.run(
                f"sed -i '' 's/month = {month}/month = {{{month}}}/g' {bib_fix_path}",
                shell=True,
            )
        return bib_fix_path

    def read_bib(self):
        bib_fix_path = self.fix_bibtex()
        with open(bib_fix_path) as bibtex_file:
            bib = bibtexparser.load(bibtex_file).entries
        doi_cite_keys = {}
        for entry in bib:
            doi_cite_keys[entry["doi"]] = entry["ID"]
        return doi_cite_keys

    def get_citation_key(self):
        # TODO read exported bib file and get the citation key - compare DOIs to get the correct key
        try:
            doi_cite_keys = self.read_bib()
            cite_key = doi_cite_keys[self.doi]
            # @citekey = user.citekey in dendrn. Wiki link used to show exact cite key
            cite_key_wiki = f"[[{cite_key}|user.{cite_key}]]"
        except KeyError:
            cite_key_wiki = "No citation key"
            log.warning(
                f"No citation key for {self.title_dendron}, Check bib file is updated, if not run export in Zotero."
            )
        return cite_key_wiki

    def get_citations(self):
        try:
            extras = self.metadata['data']['extra'].split('\n')
            citations = [i for i in extras if "citations" in i]
            citations = citations[0].split("citations: ")[-1]
        except IndexError:
            citations = "No citations"
        return citations

    def get_pinned_citation_key(self):
        try:
            extras = self.metadata['data']['extra'].split('\n')
            citation_key = [i for i in extras if "Citation Key" in i]
            citation_key = citation_key[0].split("Citation Key: ")[-1]
            citation_key_wiki = f"[[{citation_key}|user.{citation_key}]]"
        except Exception as e:
            # Not sure which error is going to be triggered here
            log.warning(
                f"No citation key for {self.title_dendron}, Check that citation keys are being pinned in Zotero."
            )
        return citation_key_wiki

    def get_publication_title(self):
        try:
            publication_title = self.metadata["data"]["publicationTitle"]
            publication_title_dendron = "-".join(publication_title.split(" "))
            link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.publication-title.{publication_title_dendron}"
            publication_title_wiki = f"[[{publication_title}|{link}]]"
        except KeyError:
            publication_title_wiki = "No publication title"
        return publication_title_wiki

    def get_journal_abbreviation(self):
        journal_abbreviation = self.metadata["data"]["journalAbbreviation"]
        journal_abbreviation_den = "-".join(journal_abbreviation.split(" "))
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.publication-title.{journal_abbreviation_den}"
        journal_abbreviation_wiki = f"[[{journal_abbreviation}|{link}]]"
        return journal_abbreviation_wiki

    def get_item_type(self):
        item_type = self.metadata["data"]["itemType"]
        item_type_den = "-".join(item_type.split(" "))
        link = f"dendron://{PROJECT_DIR}/{DENDRON_LIMB}.item-type.{item_type_den}"
        item_type_wiki = f"[[{item_type}|{link}]]"
        return item_type_wiki

    def get_pdf_attachments(self):
        # TODO for groups only - need another for local. parameterize type of library.
        # TODO deal with multiple attachments... like supplementary.
        group = True
        if group:
            try:
                attachment = [
                    str(v).split("/")[-1]
                    for k, v in self.metadata["links"]["attachment"].items()
                    if k == "href"
                ][0]
                link = f"https://www.zotero.org/groups/{self.id}/{self.name}/items/{self.id}/attachment/{attachment}/reader"
                self.attachment_id = attachment
                pdf_attachment = f"[Online PDF attachment]({link})"
            except KeyError:
                pdf_attachment = None
                log.warning(
                    "No PDF attachment... Your metadata should probably have attachments."
                )
        return pdf_attachment

    def get_tags(self):
        for tags in self.metadata["data"]["tags"]:
            if " " in tags["tag"]:
                log.warning(
                    f"Tags should not contain spaces. Please remove spaces in Zotero and sync again. Tag: {tags['tag']}. Title Dendron: {self.title_dendron}."
                )
        tags = ", ".join([f"#{i['tag']}" for i in self.metadata["data"]["tags"]])
        # TODO Config to convert tags that aren't delimited by '-' to be... On backward sync they can be updated with this. Could be a dangerous operation
        return tags

    def get_local_library(self):
        local_library = f"zotero://select/items/{self.id}"
        local_library_wiki = f"[Local Library]({local_library})"
        return local_library_wiki

    def get_cloud_library(self):
        cloud_library = f"https://www.zotero.org/groups/{self.id}/{self.name}/library"
        cloud_library_wiki = f"[Cloud Library]({cloud_library})"
        return cloud_library_wiki

    def get_abstract(self):
        abstract = self.metadata["data"]["abstractNote"]
        return abstract


class MetadataCompiler:
    def __init__(self, title_dendron: str = None) -> list:
        self.title_dendron = title_dendron
        self.lines: list = None

    def get_local_metadata_link(self):
        limb_split = DENDRON_LIMB.replace("import", "local")
        local_metadata_link = (
            f"dendron://{PROJECT_DIR}/{limb_split}.{self.title_dendron}.md"
        )
        local_metadata_link_wiki = f"[[Local Note|{local_metadata_link}]]"
        return local_metadata_link_wiki

    def compile(self, metadata):
        lines = []
        # TODO implement config
        config = True
        lines.append("## Metadata\n")
        if config is not None:
            lines.append(f"- Title: {metadata.get_title()}")
        if config is not None:
            lines.append(f"- Authors: {metadata.get_creators()}")
        if config is not None:
            lines.append(f"- Date: {metadata.get_date()}")
        if config is not None:
            lines.append(f"- Date Accessed: {metadata.get_access_date()}")
        if config is not None:
            lines.append(f"- Date Added: {metadata.get_date_added()}")
        if config is not None:
            lines.append(f"- Date Modified: {metadata.get_date_modified()}")
        if config is not None:
            lines.append(f"- URL: {metadata.get_url()}")
        if config is not None:
            lines.append(f"- DOI: {metadata.get_DOI()}")
        # TODO remove citation key
        # if config is not None:
        #     lines.append(f"- Cite Key: {metadata.get_citation_key()}")
        ### TODO
        if config is not None:
            lines.append(f"- Citation Key: {metadata.get_pinned_citation_key()}")
        if config is not None:
            lines.append(f"- Citations: {metadata.get_citations()}")
        ###
        if config is not None:
            lines.append(f"- Publication Title: {metadata.get_publication_title()}")
        if config is not None:
            lines.append(f"- Journal Abbreviation: {metadata.get_publication_title()}")
        if config is not None:
            lines.append(f"- Item Type: {metadata.get_item_type()}")
        if config is not None:
            lines.append(f"- PDF Attachments: {metadata.get_pdf_attachments()}")
        if config is not None:
            lines.append(f"- Tags: {metadata.get_tags()}")
        if config is not None:
            lines.append(f"- Local Library: {metadata.get_local_library()}")
        if config is not None:
            lines.append(f"- Cloud Library: {metadata.get_cloud_library()}")
        if config is not None:
            lines.append("\n## Abstract")
            lines.append(metadata.get_abstract())
        if config is not None:
            lines.append("\n## Local Note")
            lines.append(self.get_local_metadata_link())
        self.lines = lines
        return lines

    def write_metadata(self):
        path = [POD_PATH]
        path.extend(DENDRON_LIMB.split("."))
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        with open(osp.join(path, f"{self.title_dendron}.md"), "w") as f:
            for line in self.lines:
                f.write(line)
                f.write("\n")


##############----------Annotations----------################
@dataclass
class Annotation:
    annotation: dict = None
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
            annotation_author_name = self.annotation["data"]["annotationAuthorName"]
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
        # TODO implement cfg
        cfg_annotations_tags_format = True
        if annotation_tags != "":
            if cfg_annotations_tags_format:
                lines.append(f"- Tags: {annotation_tags}")
        return lines

    def format_annotation_text(self, lines: list, annotation_text: str):
        # needs newline before and after to render block quote properly
        lines.append(f"\n> {annotation_text}")
        return lines

    def get_annotation_link(self):
        # TODO only works in local library
        pass

    def get_date_added(self):
        date_added = utc_parse(self.annotation["data"]["dateAdded"])
        return date_added


class AnnotationsCompiler:
    def __init__(self, title_dendron: str = None):
        self.title_dendron = title_dendron
        self.lines: list = None

    def get_local_annotation_link(self):
        limb_split = DENDRON_LIMB.replace("import", "local")
        local_annotations_link = (
            f"dendron://{PROJECT_DIR}/{limb_split}.{self.title_dendron}.comments"
        )
        local_annotations_link_wiki = f"[[Local Note|{local_annotations_link}]]"
        return local_annotations_link_wiki

    def compile(self, annotations: list = None) -> list:
        lines = []
        lines.append("## Annotations")
        # save annotations to txt file
        # TODO default sort order is ['data']['dateModified']. Add config to allow for
        for i, annot in enumerate(annotations):
            annot = Annotation(annot)
            # TODO separate out all of these into their own functions
            # annotation_keys.append(i['key'])
            # lines.append(annot['data']['annotationPageLabel'])
            date_added = annot.get_date_added()
            lines.append(f"\n### Date Added: {date_added}")
            annotation_text = annot.get_annotation_text()
            lines = annot.format_annotation_text(lines, annotation_text)
            lines.append("")
            lines.append(f"- Annotator: @{annot.get_annotation_author_name()}")
            color_emoji = annot.get_color()
            annotation_comment = annot.get_annotation_comment()
            lines = annot.format_annotation_comment(
                lines, annotation_comment, color_emoji, color_emoji_cfg=True
            )
            tags = annot.get_annotation_tags()
            lines = annot.format_annotation_tags(lines, tags)
        lines.append("\n## Local Note")
        lines.append(f"- {self.get_local_annotation_link()}")
        self.lines = lines
        return lines

    def write_annotations(self):
        path = [POD_PATH]
        path.extend(DENDRON_LIMB.split("."))
        path.append(self.title_dendron)
        # path = "/".join(path)
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        with open(osp.join(path, f"annotations.md"), "w") as f:
            for line in self.lines:
                f.write(line)
                f.write("\n")


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    # TODO add to configs
    api_key = cfg.api_key
    library_id = cfg.library_id
    library_type = cfg.library_type  # or 'user'
    zot = zotero.Zotero(library_id, library_type, api_key)
    # Allowing for Collection Import - This will be a more useful feature than importing the entire library.
    metadata_list = []
    if cfg.collection is not None:
        collection_key = [
            i for i in zot.collections() if i["data"]["name"] == cfg.collection
        ][0]["key"]
        items = zot.collection_items(collection_key)
        for i in items:
            if i["data"]["itemType"] in cfg.item_types:
                metadata_list.append(i)
    if cfg.collection is None:
        for i in zot.everything(zot.items()):
            # TODO adding in books, preprints, collections, etc.
            # Relvevant to my lib for quick fix (guess based on looking at Zotero and knowing that the API uses camelCase)): "preprint", "report", "software", "webPage"
            # TODO having multiple lists of item types is redundant. This should be a default Hydra parameter.
            if i["data"]["itemType"] in ["journalArticle", "book"]:
                metadata_list.append(i)
    log.info("Extracting Data Per entry")
    for metadata in tqdm(metadata_list):
        # metadata
        # TODO fix first
        # BUG defaulted showing up. Follow metadata. Not initialized properly.
        meta = Metadata(metadata)
        meta_compiler = MetadataCompiler(meta.title_dendron)
        meta_compiler.compile(meta)
        meta_compiler.write_metadata()
        # annotations
        annotations = zot.children(meta.attachment_id)
        annot_compiler = AnnotationsCompiler(meta.title_dendron)
        annot_compiler.compile(annotations)
        annot_compiler.write_annotations()
    # HACK Caching
    itemType = ["journalArticle"]
    itemType = (" || ").join(itemType)
    cache_dir = "zendron_cache"
    if not osp.exists(cache_dir):
        os.makedirs(cache_dir)
    with open(osp.join(cache_dir, "metadata_cache.json"), "w") as f:
        cache = zot.item_versions(itemType=itemType)
        json.dump(cache, f, indent=4)
    itemType = ["annotation"]
    with open(osp.join(cache_dir, "annotations_cache.json"), "w") as f:
        cache = zot.item_versions(itemType=itemType)
        json.dump(cache, f, indent=4)


if __name__ == "__main__":
    main()
