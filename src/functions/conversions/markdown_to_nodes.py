from enum import Enum
from logging import Logger
from re import A
from src.functions.conversions.node_to_html import text_to_textnodes
from src.nodes.leafnode import LeafNode
from src.nodes.parentnode import ParentNode

from src.nodes.textnode import TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block) -> BlockType:
    if block.startswith("#"):
        return BlockType.HEADING

    if block.startswith("```\n") and block[-3:] == "```":
        return BlockType.CODE

    if block.startswith(">"):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("1."):
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


def text_nodes_repr(nodes):
    node_repr_fmt = "TextNode(Text={text}, TextType={text_type}, URL={url})"
    return_str = ""
    for node in nodes:
        return_str += (
            node_repr_fmt.format(text=node.text, text_type=node.text_type, url=node.url)
            + "\n"
        )

    return return_str[:-1]


def markdown_to_text_nodes(markdown, logger: Logger) -> list[TextNode]:
    blocks = markdown_to_blocks(markdown)
    block_type_pairs = []
    for block in blocks:
        block_type_pairs.append((block_to_block_type(block), block))

    text_nodes = []
    for block_type, block in block_type_pairs:
        # TODO: determine if the block being 0 len means it needs a newline / space added...
        if len(block) == 0:
            # print("DEBUG -- block is len 0 --> context", blocks)
            continue

        logger.info(f"Block: {block}")
        block_text_nodes = text_to_textnodes(block)
        text_nodes.extend(block_text_nodes)

        logger.info(
            f"Converted to text node list.\n[{text_nodes_repr(block_text_nodes)}]"
        )
    return text_nodes


def text_nodes_to_html(nodes, logger: Logger) -> ParentNode:

    children_html_nodes = []

    return ParentNode(tag="div", children=children_html_nodes, props=None)


def markdown_to_html(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_type_pairs = []
    for block in blocks:
        block_type_pairs.append((block_to_block_type(block), block))

    html_nodes = []
    for block_type, block in block_type_pairs:
        if len(block) == 0:
            continue

        match block_type:
            case BlockType.PARAGRAPH:
                children = children_html_nodes_from_block(block.replace("\n", " "))
                html_nodes.append(
                    parent_node_from_children_nodes(tag="p", children=children)
                )
            case BlockType.CODE:
                code_html_node = html_node_from_code_block(block)
                html_nodes.append(ParentNode(tag="pre", children=[code_html_node]))
            case BlockType.QUOTE:
                children = children_html_nodes_from_block(block)
                html_nodes.append(
                    parent_node_from_children_nodes(tag="blockquote", children=children)
                )
            case BlockType.UNORDERED_LIST:
                children = children_text_nodes_from_block(block)
                children = [
                    text_node_to_list_item(child_text_node)
                    for child_text_node in children
                ]
                html_nodes.append(
                    parent_node_from_children_nodes(tag="ul", children=children)
                )
            case BlockType.ORDERED_LIST:
                children = children_text_nodes_from_block(block)
                children = [
                    text_node_to_list_item(child_text_node)
                    for child_text_node in children
                ]
                html_nodes.append(
                    parent_node_from_children_nodes(tag="ol", children=children)
                )
            case BlockType.HEADING:
                text_node = text_to_textnodes(block)[0]
                html_nodes.append(text_node_to_heading_html_node(text_node))

    return ParentNode(tag="div", children=html_nodes)
