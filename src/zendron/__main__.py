import logging
import subprocess

from zendron import load

log = logging.getLogger(__name__)


def main():
    log.info("Sync Starting")
    load.main()
    subprocess.run("dendron importPod --podId dendron.markdown --wsRoot .", shell=True)
    subprocess.run("rm -r zotero_pod", shell=True)
    log.info("Sync Complete")


if __name__ == "__main__":
    main()


import shutil

directory_to_remove = "/path/to/directory"

try:
    shutil.rmtree(directory_to_remove)
    print(f"Directory '{directory_to_remove}' and its contents have been removed.")
except OSError as e:
    print(f"Error: {e.filename} - {e.strerror}.")
