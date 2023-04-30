import json
import logging
import os
import os.path as osp
from curses import meta
from dataclasses import dataclass, field
from datetime import datetime

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf
from pyzotero import zotero
from tqdm import tqdm

from zendron import front
from zendron.date import utc_parse
from zendron.items import get_annotated_attachments, get_attachments

# set logger
log = logging.getLogger(__name__)


@dataclass
class Metadata:
    metadata: dict = None
    attachments: dict = None
    dendron_limb: str = None
    project_dir: str = field(default=os.getcwd().split("/")[-1])
    title_dendron: str = field(init=False, repr=False)
    doi: str = field(init=False, repr=False)
    library_id: str = field(init=False, repr=False)
    key: str = field(init=False, repr=False)
    name: str = field(init=False, repr=False)
    _attachment_keys: str = field(default=None, repr=False)
    citation_key: str = field(init=False, repr=False)

    def __post_init__(self):
        self.title_dendron: str = self.get_title_dendron()
        self.library_id: str = self.metadata["library"]["id"]
        self.key: str = self.metadata["key"]
        self.name: str = self.metadata["library"]["name"]

    def get_title_dendron(self):
        title = self.metadata["data"]["title"]
        title = title.replace(":", "-")  # HACK should belong in a formatter
        title_dendron = "-".join(title.split(" "))
        return title_dendron

    def get_title(self):
        title = self.metadata["data"]["title"]
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.title.{self.title_dendron}"
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
            link = (
                f"dendron://{self.project_dir}/{self.dendron_limb}.authors.{name_den}"
            )
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
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.date.{date_dendron}"
        date_wiki = f"[[{date}|{link}]]"
        return date_wiki

    def get_access_date(self):
        try:
            access_date = utc_parse(self.metadata["data"]["accessDate"])
            access_date = str(access_date).split(" ")[0]
            date_dendron = access_date.replace("-", ".")
            link = (
                f"dendron://{self.project_dir}/{self.dendron_limb}.date.{date_dendron}"
            )
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
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.date.{date_dendron}"
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
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.date.{date_dendron}"
        date_modified_wiki = f"[[{date_modified}|{link}]]"
        return date_modified_wiki

    def get_url(self):
        url = self.metadata["data"]["url"]
        if url == "":
            return "No URL"
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

    def get_citations(self):
        try:
            extras = self.metadata["data"]["extra"].split("\n")
            citations = [i for i in extras if "citations" in i]
            citations = citations[0].split("citations: ")[-1]
        except IndexError:
            citations = "No citations"
        return citations

    def get_pinned_citation_key(self):
        try:
            extras = self.metadata["data"]["extra"].split("\n")
            citation_key = [i for i in extras if "Citation Key" in i]
            self.citation_key = citation_key[0].split("Citation Key: ")[-1]
            citation_key_wiki = f"[[{self.citation_key}|user.{self.citation_key}]]"
        except Exception as e:
            # Not sure which error is going to be triggered here
            log.warning(
                f"No citation key for {self.title_dendron}, Check that citation keys are being pinned in Zotero."
            )
        return citation_key_wiki

    def get_publication_title(self):
        try:
            publication_title = self.metadata["data"]["publicationTitle"]
            publication_title = publication_title.replace("[", "").replace(
                "]", ""
            )  # HACK needs to go into formatter
            publication_title_dendron = "-".join(publication_title.split(" "))
            link = f"dendron://{self.project_dir}/{self.dendron_limb}.publication-title.{publication_title_dendron}"
            publication_title_wiki = f"[[{publication_title}|{link}]]"
        except KeyError:
            publication_title_wiki = "No publication title"
        return publication_title_wiki

    def get_journal_abbreviation(self):
        journal_abbreviation = self.metadata["data"]["journalAbbreviation"]
        journal_abbreviation_den = "-".join(journal_abbreviation.split(" "))
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.publication-title.{journal_abbreviation_den}"
        journal_abbreviation_wiki = f"[[{journal_abbreviation}|{link}]]"
        return journal_abbreviation_wiki

    def get_item_type(self):
        item_type = self.metadata["data"]["itemType"]
        item_type_den = "-".join(item_type.split(" "))
        link = f"dendron://{self.project_dir}/{self.dendron_limb}.item-type.{item_type_den}"
        item_type_wiki = f"[[{item_type}|{link}]]"
        return item_type_wiki

    @property
    def attachment_keys(self):
        if self._attachment_keys is None:
            self._attachment_keys = [i["key"] for i in self.attachments]
        return self._attachment_keys

    def get_pdf_attachments(self):
        # TODO for groups only - need another for local. parameterize type of library.
        # TODO deal with multiple attachments... like supplementary.
        library_type = self.metadata["library"]["type"]
        if library_type == "user":
            pdf_attachment = None
            for att_key in self.attachment_keys:
                try:
                    link = f"https://www.zotero.org/{self.name}/items/{self.key}/attachment/{att_key}/reader"
                    pdf_attachment = f"[Online PDF attachment]({link})"
                except KeyError:
                    pdf_attachment = None
                    log.warning(
                        "No PDF attachment... Your metadata should probably have attachments."
                    )
        if library_type == "group":
            pdf_attachment = None
            for att_key in self.attachment_keys:
                try:
                    # TODO check if this works for groups
                    link = f"https://www.zotero.org/groups/{self.library_id}/zendron/items/{self.key}/attachment/{att_key}/reader"
                    pdf_attachment = f"[Online PDF attachment]({link})"
                except KeyError:
                    pdf_attachment = None
                    log.warning(
                        "No PDF attachment... Your metadata should probably have attachments."
                    )
        return pdf_attachment

    def get_tags(self):
        if self.metadata["data"]["tags"] == []:
            return "No tags"
        for tags in self.metadata["data"]["tags"]:
            if " " in tags["tag"]:
                log.warning(
                    f"Tags should not contain spaces. Please remove spaces in Zotero metadata and sync again. Tag: {tags['tag']}. Title Dendron: {self.title_dendron}."
                )
        tags = ", ".join([f"#{i['tag']}" for i in self.metadata["data"]["tags"]])
        # TODO Config to convert tags that aren't delimited by '-' to be... On backward sync they can be updated with this. Could be a dangerous operation
        return tags

    def get_local_library(self):
        local_library = f"zotero://select/items/{self.library_id}"
        local_library_wiki = f"[Local Library]({local_library})"
        return local_library_wiki

    def get_cloud_library(self):
        cloud_library = (
            f"https://www.zotero.org/groups/{self.library_id}/{self.name}/library"
        )
        cloud_library_wiki = f"[Cloud Library]({cloud_library})"
        return cloud_library_wiki

    def get_abstract(self):
        abstract = self.metadata["data"]["abstractNote"]
        if abstract == "":
            abstract = "No abstract"
        return abstract


class MetadataCompiler:
    def __init__(self, metadata: Metadata = None, pod_path: str = None):
        self.metadata = metadata
        self.pod_path = pod_path
        self.lines: list = None

    def compile(self) -> str:
        lines = []
        # TODO implement config for adding different data.
        lines.append("## Metadata\n")
        lines.append(f"- Title: {self.metadata.get_title()}")
        lines.append(f"- Authors: {self.metadata.get_creators()}")
        lines.append(f"- Date: {self.metadata.get_date()}")
        lines.append(f"- Date Accessed: {self.metadata.get_access_date()}")
        lines.append(f"- Date Added: {self.metadata.get_date_added()}")
        lines.append(f"- Date Modified: {self.metadata.get_date_modified()}")
        lines.append(f"- URL: {self.metadata.get_url()}")
        lines.append(f"- DOI: {self.metadata.get_DOI()}")
        lines.append(f"- Citation Key: {self.metadata.get_pinned_citation_key()}")
        lines.append(f"- Citations: {self.metadata.get_citations()}")
        lines.append(f"- Publication Title: {self.metadata.get_publication_title()}")
        lines.append(f"- Journal Abbreviation: {self.metadata.get_publication_title()}")
        lines.append(f"- Item Type: {self.metadata.get_item_type()}")
        lines.append(f"- PDF Attachments: {self.metadata.get_pdf_attachments()}")
        lines.append(f"- Tags: {self.metadata.get_tags()}")
        lines.append(f"- Local Library: {self.metadata.get_local_library()}")
        lines.append(f"- Cloud Library: {self.metadata.get_cloud_library()}")
        lines.append("\n## Abstract\n")
        lines.append(self.metadata.get_abstract())
        self.lines = lines
        return lines

    def write(self):
        path = [self.pod_path]
        path.extend(self.metadata.dendron_limb.split("."))
        path = "/".join(path)
        os.makedirs(path, exist_ok=True)
        file_path = osp.join(path, f"{self.metadata.title_dendron}.md")
        with open(file_path, "w") as f:
            for line in self.lines:
                f.write(line)
                f.write("\n")
        front.add_metadata_key(self.metadata.key, file_path)


def main():
    pass


if __name__ == "__main__":
    main()
