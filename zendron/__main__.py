import argparse
import logging
import os
import os.path as osp
import subprocess
import sys
import yaml
import hydra
from omegaconf import DictConfig

from zendron import init, load, load_since_cache

log = logging.getLogger(__name__)

# Pre-processing for --remove flag
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-rm", "--remove", action="store_true")
parser.add_argument("-nc", "--no-cache", action="store_true")
args, remaining_argv = parser.parse_known_args()
sys.argv[1:] = remaining_argv  # Pass the remaining arguments to Hydra

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
    if args.remove:
        from zendron import remove

        log.info("Remove Starting")
        remove.main(cfg)
    elif args.no_cache:
        log.info("Sync Starting (no cache)")
        load.main(cfg)
        subprocess.run(
            f"dendron importPod --podId dendron.markdown --wsRoot .", shell=True
        )
        subprocess.run(f"rm -r {pod_path}", shell=True)
        log.info("Sync Complete")
    else:
        log.info("Sync Starting")
        is_new_data = load_since_cache.main(cfg)
        if is_new_data:
            subprocess.run(
                f"dendron importPod --podId dendron.markdown --wsRoot .", shell=True
            )
            subprocess.run(f"rm -r {pod_path}", shell=True)
            log.info("Sync complete")
        else:
            log.info("No new data to sync. Exiting.")


if __name__ == "__main__":
    main()
