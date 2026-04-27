from pathlib import Path
from logging import Logger

from os import path, listdir, makedirs
from shutil import copy, rmtree
from src.functions.generate_page import generate_page
from src.const import PUBLIC, STATIC, LOGGING
from collections import deque


def prep_public_dir(logger):
    ## DELETE public
    logger.info(f"rmtree on public: {PUBLIC}")
    rmtree(PUBLIC)
    if path.exists(PUBLIC):
        raise Exception("rmtree failed to rm the public directory")

    ## CREATE public
    logger.info("Attempting to make new public dir")
    makedirs(PUBLIC)
    if not path.exists(PUBLIC):
        raise Exception(f"makedirs failed on public path: {PUBLIC}")
    logger.info(f"Attempt succeeded: {PUBLIC} exists.")


def copy_all(source_dir: Path, dest_dir: Path, logger: Logger):
    ## INIT queue
    logger.info(f"Init deque with source_dir: {source_dir}")
    dir_queue = deque()
    dir_queue.append(source_dir)

    while dir_queue:
        ## POP dir and copy files, queue directories
        current_dir = dir_queue.pop()
        logger.info(f"current_dir: {current_dir}")

        for file in listdir(current_dir):
            # Full filepath preserved across all layers from first iteration having full path
            file_path = current_dir / file

            ## QUEUE dir
            logger.info(f"Inspecting filepath: {file_path}")
            if not path.isfile(file_path) and path.isdir(file_path):
                logger.info(f"Directory found {file_path} -- adding to queue")
                dir_queue.append(file_path)
                continue

            ## RELATIVE PATH to static
            # Ex: file: static/content/index.md
            # relpath file to static: content/index.md
            # relative_dir = path.split(relpath) --> "content"
            #
            # use makedirs(relative_dir, exists_ok=True) to create
            relative_path = path.relpath(file_path, STATIC)
            relative_dir = path.split(relative_path)[0]
            logger.info(f"relative path to static: {relative_path}")

            # Given this behavior, we can just append the relative dir
            # Path("abc") / "" ==> Path("abc")

            ## GENERATE destination filepath in public
            destination = PUBLIC / relative_dir / file
            destination_dir = PUBLIC / relative_dir
            logger.info(f"Dest Filepath from file({file}) is {destination}")

            if not path.exists(destination_dir):
                logger.info(
                    f"makedirs, exists_ok called for destination_dir: {destination_dir}"
                )
                makedirs(destination_dir, exist_ok=True)

            # Now dir exists (if it didnt before) copy file to public on the relative path
            copied = copy(file_path, destination)
            logger.info(f"File copied from {file_path} to {copied}")
        logger.info(f"Fully iterated over current dir: {current_dir}")
    logger.info("Finished queue of directories.")
