import logging
import os
import os.path as osp
import shutil

import zendron

# set logger
log = logging.getLogger(__name__)


from omegaconf import OmegaConf


def load_default_config():
    workspace_root = os.getcwd()
    default_config_path = osp.join(workspace_root, "conf", "default.yaml")
    return OmegaConf.load(default_config_path)


def is_initialized() -> bool:
    default_config = load_default_config()
    return default_config.initialized


def set_initialized():
    default_config = load_default_config()
    default_config.initialized = True
    workspace_root = os.getcwd()
    default_config_path = osp.join(workspace_root, "conf", "default.yaml")
    OmegaConf.save(default_config, default_config_path)


def main():
    if not is_initialized():
        package_root = osp.dirname(osp.abspath(zendron.__file__))

        # List all the config files and their paths within the package
        config_files = [
            "conf/__init__.py",
            "conf/config.yaml",
            "conf/default.yaml",
            "conf/config_template.yaml",
            "pods/custom/dendron.markdown/config.import.yml",
        ]

        # Copy each config file to the user's workspace root directory
        for file_path in config_files:
            src_path = osp.join(package_root, file_path)
            dest_path = osp.join(os.getcwd(), file_path)

            # Ensure the destination folder exists
            dest_folder = osp.dirname(dest_path)
            os.makedirs(dest_folder, exist_ok=True)

            if not osp.exists(dest_path):
                shutil.copy2(src_path, dest_path)
                print(f"{file_path} has been copied to the workspace root directory.")
            else:
                print(f"{file_path} already exists in the workspace root directory.")
            set_initialized()
            log.info("Initialization complete.")
    else:
        log.info(f"Zendron has already been initialized.")


if __name__ == "__main__":
    main()
