import argparse
import logging
import os
import os.path as osp
import subprocess

import hydra
from omegaconf import DictConfig

from zendron import init, load

log = logging.getLogger(__name__)

global USER_CONFIGURE
USER_CONFIGURE = False

if init.user_configure():
    USER_CONFIGURE = True


@hydra.main(
    version_base=None,
    config_path=osp.join(os.getcwd(), "conf", "zendron"),
    config_name="config",
)
def main(cfg: DictConfig) -> None:
    if USER_CONFIGURE:
        return
    elif cfg.remove:
        from zendron import remove

        log.info("Remove Starting")

        remove.main(cfg)
    else:
        log.info("Sync Starting")
        load.main(cfg)
        subprocess.run(
            "dendron importPod --podId dendron.markdown --wsRoot .", shell=True
        )
        subprocess.run("rm -r zotero_pod", shell=True)
        log.info("Sync Complete")


if __name__ == "__main__":
    main()
