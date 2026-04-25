from src.logger import get_logger
from pathlib import Path
from os import path, listdir, makedirs
from shutil import copy, rmtree
from src.functions.generate_page import generate_page
from collections import deque


def main():
    logger = get_logger("dir_operations.log")

    home = Path("/home/cjester/Code/StaticSiteGenerator")
    public = home / "public"
    static = home / "static"
    content_path = static / "content"

    logger.info(f"Init paths home, public, static:\n{home}\n{public}\n{static}")

    logger.info(f"rmtree on public: {public}")
    rmtree(public)

    if path.exists(public):
        raise Exception("rmtree failed to rm the public directory")

    logger.info("Attempting to make new public dir")
    makedirs(public)
    if not path.exists(public):
        raise Exception(f"makedirs failed on public path: {public}")
    logger.info(f"Attempt succeeded: {public} exists.")

    logger.info(f"Init deque with static dir: {static}")
    dir_queue = deque()
    dir_queue.append(static)

    while dir_queue:
        current_dir = dir_queue.pop()
        logger.info(f"current_dir: {current_dir}")

        for file in listdir(current_dir):
            file_path = current_dir / file

            logger.info(f"Inspecting filepath: {file_path}")
            if not path.isfile(file) and path.isdir(file_path):
                logger.info(f"Directory found for {file} -- adding to queue")
                dir_queue.append(file_path)
                continue

            relative_path = path.relpath(file_path, static)
            relative_dir = path.split(relative_path)[0]
            logger.info(f"relative path to static: {relative_path}")
            logger.info(f"relative directory path: {relative_dir}")

            # check dir portion exists
            if not path.exists(relative_dir) and relative_dir != "":
                logger.info(f"relative_dir does not exist: {relative_dir}")
                subdirs = relative_dir.split("/")

                for dir in subdirs:
                    if dir == "":
                        continue
                    logger.info(f"Attempting to create subdir: {dir} within public.")
                    makedirs(public / dir, exist_ok=True)

            # Now dir exists (if it didnt before) copy file to public on the relative path
            destination = copy(file_path, public / relative_path)
            logger.info(f"File copied from {file_path} to {destination}")
        logger.info(f"Fully iterated over current dir: {current_dir}")
    logger.info("Finished queue of directories.")

    generate_page(
        content_path / "index.md",
        home / "template.html",
        public / "content/index.html",
        logger,
    )


if __name__ == "__main__":
    main()
    exit()
