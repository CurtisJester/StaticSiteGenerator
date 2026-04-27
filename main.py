from src.functions.dir_utils.copy_dirs import copy_all, prep_public_dir
from src.functions.generate_page import generate_pages_recursively
from src.const import PUBLIC, STATIC, LOGGING
from src.utility.logger import get_logger

from pathlib import Path
from sys import argv


def main():
    if len(argv) == 0:
        basepath = Path("/")
    else:
        basepath = Path(argv[0])

    home = Path("/home/cjester/Code/boot.dev/StaticSiteGenerator")
    content_dir_path = home / "content"
    template_file_path = home / "template.html"
    logger = get_logger("dir_operations.log", LOGGING)

    prep_public_dir(logger)
    copy_all(STATIC, PUBLIC, logger)

    generate_pages_recursively(
        dir_path_content=content_dir_path,
        template_path=template_file_path,
        dest_dir_path=PUBLIC,
        basepath=basepath,
        logger=logger,
    )
    # generate_page(index_md_path, template_path, public_index_path, logger)


if __name__ == "__main__":
    main()
    exit()
