import argparse
import logging
import os
import os.path as osp
import subprocess
import sys
import yaml
import hydra
from omegaconf import DictConfig
from zendron import remove, dry_remove
from zendron import init, load, load_since_cache

log = logging.getLogger(__name__)

def zendron_help():
    help_message = """
    zendron [OPTIONS] - A tool for syncing Zotero data with Dendron notes.

        1. Run after changes in Zotero collection to sync to Dendron notes.
        2. Run after changes to local comments notes to sync to Zotero.

    Options:
      -drm, --dry-remove    Perform a dry run of the remove operation without actually deleting files.
      -rm,  --remove        Remove files based on Zendron's configuration.
      -nc,  --no-cache      Perform synchronization without using the cache.
      -h,   --help          Display this help message.
    """
    print(help_message)

# Pre-processing for custom flags
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-drm", "--dry-remove", action="store_true")
parser.add_argument("-rm", "--remove", action="store_true")
parser.add_argument("-nc", "--no-cache", action="store_true")
parser.add_argument("-h", "--help", action="store_true")
args, remaining_argv = parser.parse_known_args()

# If the user requests Zendron-specific help, display it and exit
if args.help:
    zendron_help()
    sys.exit()

sys.argv[1:] = remaining_argv  # Pass the remaining arguments to Hydra for further processing

# Adjust the global USER_CONFIGURE based on the configuration utility
global USER_CONFIGURE
USER_CONFIGURE = init.user_configure()

@hydra.main(
    version_base=None,
    config_path=osp.join(os.getcwd(), "conf", "zendron"),
    config_name="config",
)
def main(cfg: DictConfig) -> None:
    if USER_CONFIGURE:
        return

    # Determine the operation mode based on the --remove flag
    if args.dry_remove:
        log.info("Dry remove Starting")
        dry_remove.main(cfg)
    elif args.dry_remove:
        log.info("Dry remove Starting")
        dry_remove.main(cfg)
    elif args.remove:
        log.info("Remove Starting")
        remove.main(cfg)
    elif args.no_cache or not osp.exists(".zendron.cache.json"):
        log.info("Sync Starting")
        load.main(cfg)
        subprocess.run(
            f"dendron importPod --podId dendron.markdown --wsRoot .", shell=True
        )
        subprocess.run(f"rm -r {cfg.pod_path}", shell=True)
        log.info("Sync Complete")
    else:
        log.info("Sync Starting")
        is_new_data = load_since_cache.main(cfg)
        if is_new_data:
            subprocess.run(
                f"dendron importPod --podId dendron.markdown --wsRoot .", shell=True
            )
            subprocess.run(f"rm -r {cfg.pod_path}", shell=True)
            log.info("Sync complete")
        else:
            log.info("No new metadata or annotations to sync. Exiting.")


if __name__ == "__main__":
    main()
