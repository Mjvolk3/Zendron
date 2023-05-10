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
    default_config_path = osp.join(workspace_root, "conf", "zendron", "default.yaml")
    if not osp.exists(default_config_path):
        return False
    return OmegaConf.load(default_config_path)


def is_initialized() -> bool:
    try:
        is_zendron_initialized = load_default_config().initialized
    except:
        is_zendron_initialized = False
    return is_zendron_initialized


def set_initialized():
    default_config = load_default_config()
    default_config.initialized = True
    workspace_root = os.getcwd()
    default_config_path = osp.join(workspace_root, "conf", "zendron", "default.yaml")
    OmegaConf.save(default_config, default_config_path)

    # Update config.import.yml with desired values
    config_path = osp.join(
        workspace_root, "pods", "dendron.markdown", "config.import.yml"
    )
    config = OmegaConf.load(config_path)
    config.vaultName = workspace_root.split("/")[-1]
    OmegaConf.save(config, config_path)


def user_configure() -> None:
    if not is_initialized():
        package_root = osp.dirname(osp.abspath(zendron.__file__))
        # package_root = "/".join(package_root.split("/")[:-2])
        # List all the config files and their paths within the package
        config_files = [
            "conf/zendron/__init__.py",
            "conf/zendron/default_template.yaml",
            "conf/zendron/config_template.yaml",
            "pods/dendron.markdown/config.import.yml",
        ]

        # Copy each config file to the user's workspace root directory
        for file_path in config_files:
            src_path = osp.join(package_root, file_path)
            dest_base_path, file_ext = osp.splitext(file_path)
            dest_base_path = dest_base_path.replace("_template", "")
            dest_path = osp.join(os.getcwd(), dest_base_path + file_ext)

            # Ensure the destination folder exists
            dest_folder = osp.dirname(dest_path)
            os.makedirs(dest_folder, exist_ok=True)

            if not osp.exists(dest_path):
                shutil.copy2(src_path, dest_path)
                print(f"{file_path} has been copied to the workspace root directory.")
            else:
                print(f"{file_path} already exists in the workspace root directory.")
        set_initialized()
        print("Initialization complete.")
        print(
            "Manually set the STARTER CONFIG in './conf/config.yaml' for quickstart and rerun zendron. All other configs are optional."
        )
        return True
    else:
        print("Zendron has already been initialized.")
        return False


if __name__ == "__main__":
    user_configure()
