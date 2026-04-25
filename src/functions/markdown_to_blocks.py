from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block) -> BlockType:
    if block.startswith("# "):
        return BlockType.HEADING

    if block.startswith("```\n") and block[-3:] == "```":
        return BlockType.CODE

    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("."):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("."):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    if block.startswith("-"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("-"):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown) -> list[str]:
    return [section.strip() for section in markdown.split("\n\n")]
