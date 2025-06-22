import json
import logging
import os

logger = logging.getLogger(__name__)

def find_directory_from_name(name: str) -> str:
    for dirpath, dirname, _ in os.walk(os.path.expanduser("~")):
        if name in dirname:
            return os.path.join(dirpath, name)
    return ""

REVERSE_EXTENSION_LOOKUP: dict[str, str] = {}
TARGET_DIRECTORY_LOOKUP: dict[str, (str, bool)] = {} # type: ignore

with open(os.path.abspath("config.json")) as f:
    data = json.load(f)

for directory_name in data:
    directory_path = find_directory_from_name(directory_name)
    if directory_path:
        TARGET_DIRECTORY_LOOKUP[directory_name] = (directory_path, data[directory_name]["preserve"]) 
    else:
        TARGET_DIRECTORY_LOOKUP[directory_name] = (os.path.join(os.path.expanduser("~"), directory_name), data[directory_name]["preserve"])\

    for extension in data[directory_name]["extensions"]:
        if "." not in extension and extension.lower() != "directory":
            extension = "." + extension
        REVERSE_EXTENSION_LOOKUP[extension.lower()] = directory_name

for directory_name, options in TARGET_DIRECTORY_LOOKUP.items():
    directory_path = options[0]
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        logger.info("Created directory %s at %s", directory_name, directory_path)