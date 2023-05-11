# __init__.py

from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Version of the zendron package
__version__ = "1.1.12"

# Read URL of the Real Python feed from config file
# _cfg = tomllib.loads(resources.read_text("reader", "config.toml"))
# URL = _cfg["feed"]["url"]
URL = "https://github.com/Mjvolk3/Zendron"
