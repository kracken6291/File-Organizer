import datetime
import logging
import os
import shutil
import sys

from logging_config import setup_logging

setup_logging()

from lookups import TARGET_DIRECTORY_LOOKUP, REVERSE_EXTENSION_LOOKUP  # noqa: E402

logger = logging.getLogger(__name__)


def organize_files() -> None:
    for file in os.listdir(os.path.expanduser("~\\Downloads")):
        try:
            current_path = os.path.join(os.path.expanduser("~\\Downloads"), file)

            if os.path.isdir(current_path):
                target_dir = REVERSE_EXTENSION_LOOKUP.get("directory", "")
            else:
                extension = os.path.splitext(file)[
                    -1
                ].lower()  # lowercase becasue apple uses full caps on extensions
                target_dir = REVERSE_EXTENSION_LOOKUP.get(extension, "")

            if target_dir:
                directory_path, should_rename = TARGET_DIRECTORY_LOOKUP.get(target_dir, "")
                target_path = os.path.join(directory_path, file)
                if os.path.exists(target_path):
                    if should_rename:
                        file_name = os.path.splitext(file)[0]
                        new_current_file_name = (
                            file_name
                            + " "
                            + datetime.datetime.fromtimestamp(
                                os.path.getctime(current_path)
                            ).strftime("%m-%d-%Y")
                        )
                        new_target_file_name = (
                            file_name
                            + " "
                            + datetime.datetime.fromtimestamp(
                                os.path.getctime(target_path)
                            ).strftime("%m-%d-%Y")
                        )

                        new_current_path = os.path.join(
                            os.path.expanduser("~\\Downloads"),
                            new_current_file_name + extension,
                        )
                        new_target_path = os.path.join(
                            TARGET_DIRECTORY_LOOKUP.get(target_dir, "")[0],
                            new_target_file_name + extension,
                        )

                        os.rename(current_path, new_current_path)
                        os.rename(target_path, new_target_path)
                        logger.info(
                            "renamed %s to %s in Downloads",
                            file_name,
                            new_current_file_name,
                        )
                        logger.info(
                            "renamed %s to %s in %s",
                            file_name,
                            new_target_file_name,
                            target_dir,
                        )

                        current_path = new_current_path
                        target_path = os.path.join(
                            TARGET_DIRECTORY_LOOKUP.get(target_dir, "")[0],
                            new_current_file_name + extension,
                        )
                    else:
                        logger.info("replaced %s with %s", target_path, current_path)

                if not target_path or target_path == file:
                    logger.warning(
                        "Could not move %s because directory is not in config.json", file
                    )
                else:
                    shutil.move(current_path, target_path)
                    logger.info("Moved %s from %s to %s", file, current_path, target_path)
            else:
                logger.info("Could not move %s because not in configs", file)
        except Exception as e:
            logger.warning('Could not move %s because of an error: %s', file, e)

if __name__ == "__main__":
    organize_files()
    sys.exit()
