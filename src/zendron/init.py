import logging
import os
import os.path as osp
import shutil

import hydra
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

# set logger
log = logging.getLogger(__name__)

# Put here for logging to terminal... Need to check regular python logging
@hydra.main(version_base=None, config_path="conf", config_name="config_template")
def main(cfg):
    if not osp.exists("zendron/conf/config.yaml"):
        log.info("Initializing config.yaml")
        shutil.copyfile("zendron/conf/config_template.yaml", "zendron/conf/config.yaml")
    else:
        log.info("Already initialized config.yaml")


if __name__ == "__main__":
    main()
