import logging
from pathlib import Path


def get_logger(filename):
    logger = logging.getLogger()

    file_path = Path("/home/cjester/Code/StaticSiteGenerator/logging") / filename
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
