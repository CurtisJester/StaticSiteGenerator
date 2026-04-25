from src.functions.markdown_to_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("markdown input is empty")

    blocks = markdown_to_blocks(markdown)

    title = ""
    for block in blocks:
        if BlockType.HEADING != block_to_block_type(block):
            continue

        # Not an h1 block
        if block.count("#") != 1:
            continue

        title = block.lstrip("# ")

    if title == "":
        raise Exception("no h1 heading found in markdown")
    return title
