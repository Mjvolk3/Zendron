import glob
import json
import logging
import os
import os.path as osp
import re
import shutil
import subprocess

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


def remove_files_glob(pattern: str, exclude_pattern: str = None) -> None:
    log.info(f"Removing: {pattern}")
    for matched_path in glob.glob(pattern):
        if exclude_pattern and re.search(exclude_pattern, matched_path):
            continue

        if osp.isfile(matched_path):
            try:
                os.remove(matched_path)
                print(f"File '{matched_path}' has been removed.")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")
        elif osp.isdir(matched_path):
            try:
                shutil.rmtree(matched_path)
                print(f"Directory '{matched_path}' and its contents have been removed.")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")


def citation_keys_from_cache(file_path):
    """
    Extract citation keys from a cache file.

    Args:
        file_path (str): The path to the cache JSON file.

    Returns:
        list: A list of citation keys.
    """
    with open(file_path, "r") as file:
        data = json.load(file)

    citation_keys = [entry["citation_key"] for entry in data.values()]

    return citation_keys


def main(cfg: DictConfig):
    # TODO add notes config for
    log.info("Removing all Zendron Note Files")
    remove_files_glob(f"notes/{cfg.dendron_limb}.*.md", r"\.comments\.md$")
    remove_files_glob(f"notes/{cfg.dendron_limb}.*.annotations.md")
    remove_files_glob(f"notes/{cfg.dendron_limb}.date.*.md")
    remove_files_glob(f"notes/{cfg.dendron_limb}.item-type.*.md")
    remove_files_glob(f"notes/{cfg.dendron_limb}.title.*.md")
    remove_files_glob(f"notes/{cfg.dendron_limb}.authors.*.md")

    # Get citation keys from cache.json
    cache_file_path = "zendron_cache/cache.json"
    citation_keys = citation_keys_from_cache(cache_file_path)
    citation_keys = [citation_key.lower() for citation_key in citation_keys]
    # Remove all "notes/user.citation_key.md" files except those in the citation keys list
    for file in glob.glob("notes/user.*.md"):
        citation_key = file.split("/")[-1][5:-3]
        if citation_key in citation_keys:
            remove_files_glob(file)

    # remove_files_glob("notes/tags.*.md")
    remove_files_glob("notes/assets/images/zendron-image-import-*.png")
    log.info("Removing all Zendron Cache")
    # remove_files_glob("zendron_cache/metadata_cache.json")
    # remove_files_glob("zendron_cache/annotations_cache.json")
    # log.info("Creating Missing Linked Notes with Dendron Doctor")
    # subprocess.run("dendron doctor --action createMissingLinkedNotes", shell=True)
    log.info("Note Removal Complete")


if __name__ == "__main__":
    config_file_path = osp.join(os.getcwd(), "conf", "config.yaml")
    cfg = OmegaConf.load(config_file_path)
    main(cfg)
