import logging
import os


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "fileOrganizer.log")
        ),
    )
