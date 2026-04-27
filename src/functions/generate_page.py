from logging import Logger
from pathlib import Path
from os import path, makedirs
from src.functions.extract_title import extract_title
from src.functions.markdown_to_html import markdown_to_html


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
    dest_filename, destination_path = path.split(dest_path)

    # TODO: improve this variable by providing a consts file
    # Check path is subpath to public dir
    project_path = Path("/home/cjester/Code/StaticSiteGenerator/")
    if path.relpath(dest_path, project_path).split("/")[0] != "public":
        raise Exception(
            f"Dest path ({dest_path}) is not common to project path ({project_path})"
        )

    logger.info("Path is sub-path of project path, checking directory exists")
    if not path.exists(destination_path):
        logger.info(f"Creating directory or directories: {destination_path}")
        makedirs(destination_path)

    logger.info(f"Writing updated content to file ({dest_path})")
    with open(dest_path, "w") as html_out:
        bytes = html_out.write(page_html)

    logger.info(f"({bytes}) bytes written to file.")
