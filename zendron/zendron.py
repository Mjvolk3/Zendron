import argparse
import logging
import os
import os.path as osp
import subprocess
import sys
import yaml
import hydra
from omegaconf import DictConfig

from zendron import init, load

log = logging.getLogger(__name__)

# Pre-processing for --remove flag
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-rm', '--remove', action='store_true')
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
        cfg.remove = True  # Ensure the cfg object reflects the --remove state

    if cfg.get("remove", False):  # Safely access the 'remove' key
        from zendron import remove

        log.info("Remove Starting")
        remove.main(cfg)
    else:
        with open(yaml_path, 'r') as yaml_file:
            dendron_config = yaml.safe_load(yaml_file)
            vaultName = dendron_config.get('vaultName')
        
        
        log.info("Sync Starting")
        load.main(cfg)
        subprocess.run(
            f"dendron importPod --podId dendron.markdown --wsRoot . --valut {vaultName}", shell=True
        )
        subprocess.run("rm -r zotero_pod", shell=True)
        log.info("Sync Complete")

if __name__ == "__main__":
    main()