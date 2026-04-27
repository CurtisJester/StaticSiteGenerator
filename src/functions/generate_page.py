from logging import Logger
from pathlib import Path
from os import path, makedirs, listdir
from posixpath import relpath
from re import A
from src.functions.extract_title import extract_title
from src.functions.markdown_to_html import markdown_to_html
from src.const import PUBLIC
from collections import deque


def generate_pages_recursively(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path, logger
):
    ## VALIDATIONS
    if not dir_path_content or not template_path or not dest_dir_path:
        raise Exception(
            "dir_path_content, template_path, and dest_dir_path paths are all required."
        )

    if Path(path.commonpath([PUBLIC, dest_dir_path])) != PUBLIC:
        raise Exception(
            f"Dest dir path: {dest_dir_path} is not common to Public: {PUBLIC}"
        )

    if not path.isdir(dir_path_content):
        raise Exception(f"Content Dir path is not a dir: {dir_path_content}")

    if not path.isfile(template_path):
        raise Exception(f"Template path provided is not a file: {template_path}")

    if not path.isdir(dest_dir_path):
        raise Exception(f"Destination dir path is not a dir: {dest_dir_path}")

    ## VALID
    dir_queue = deque()
    dir_queue.append(dir_path_content)

    while dir_queue:
        current_dir = dir_queue.pop()
        # Ex: project_path/content/blog/tom, current dir
        # relative_to_content <== blog/tom
        # dest_dir_path = dest_dir_path if relative_to_content == '.' else dest_dir_path / relative_to_content
        relative_to_content = path.relpath(current_dir, dir_path_content)

        new_dest_dir_path = (
            dest_dir_path
            if relative_to_content == "."
            else dest_dir_path / relative_to_content
        )
        logger.info(
            f"From dest_dir_path {dest_dir_path}, new_dest_dir_path is {new_dest_dir_path}"
        )

        logger.info(f"Processing file in current dir: {current_dir}")
        for file in listdir(current_dir):
            file_path = current_dir / file

            if path.isdir(file_path):
                dir_queue.append(file_path)
                logger.info(
                    f"generate_pages_recursively added {file_path} to dir queue"
                )
                continue
            if file[-2:] == "md":
                new_filename = file.replace("md", "html")
                generate_page(
                    file_path, template_path, new_dest_dir_path / new_filename, logger
                )
                continue

            logger.info(f"File {file} not markdown, nor dir")
        logger.info(f"Processed all files in {current_dir}")


def generate_page(from_path, template_path, dest_path, logger: Logger):
    if not from_path or not template_path or not dest_path:
        raise Exception("from, template, and destination paths are all required.")

    logger.info(
        f"Generate Page request: from({from_path}), template({template_path}), dest({dest_path})"
    )

    from_exists = path.exists(from_path) and path.isfile(from_path)
    template_exists = path.exists(template_path) and path.isfile(template_path)

    if not (from_exists and template_exists):
        raise Exception(
            f"Either from ({from_path}) or template ({template_path}) paths do not exist or are not files"
        )

    logger.info(f"Reading from file ({from_path}) and template from ({template_path})")
    with open(from_path, "r") as from_in, open(template_path, "r") as template_in:
        markdown = from_in.read()
        template = template_in.read()

    if len(markdown) == 0:
        raise Exception(f"input file ({from_path}) is empty")
    if len(template) == 0:
        raise Exception(f"template file ({template_path}) is empty")

    # Valid paths and file contents
    title = extract_title(markdown)
    node = markdown_to_html(markdown)
    logger.info(f"Title ({title}) extracted and node generated.")
    page_html = template.replace("{{ Title }}", title)

    page_html = page_html.replace("{{ Content }}", node.to_html())

    # Content is staged, destination path check
    if PUBLIC != Path(path.commonpath([dest_path, PUBLIC])):
        raise Exception(
            f"Dest path ({dest_path}) is not common to public subdir: {PUBLIC}"
        )

    logger.info("Path is sub-path of project path, checking directory exists")
    dest_dir, filename = path.split(dest_path)
    if not path.exists(dest_dir):
        logger.info(f"Creating directory or directories: {dest_dir}")
        makedirs(dest_dir, exist_ok=True)

    logger.info(f"Writing updated content to file ({dest_path})")
    with open(dest_path, "w") as html_out:
        bytes = html_out.write(page_html)

    logger.info(f"({bytes}) bytes written to file.")
