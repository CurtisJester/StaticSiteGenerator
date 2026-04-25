from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextType, TextNode
from src.nodes.htmlnode import HTMLNode
from src.nodes.parentnode import ParentNode
from src.functions.markdown_to_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
)
from src.functions.node_to_html import (
    parent_from_children,
    text_node_to_heading_html_node,
    text_node_to_list_item,
    text_node_to_html_node,
    text_to_textnodes,
    text_to_children,
)


def html_node_from_code_block(block) -> HTMLNode:
    return text_node_to_html_node(TextNode(text=block, text_type=TextType.CODE))


def children_html_nodes_from_block(block) -> list[LeafNode]:
    children = []
    for line in block.split("\n"):
        children.extend(text_to_children(line))
    return children


def children_text_nodes_from_block(block) -> list[TextNode]:
    """
    Given a block (a single/multiline str), return a list of TextNodes after
    applying inline Markdown
    """
    children = []
    for line in block.split("\n"):
        children.extend(text_to_textnodes(line))
    return children


def markdown_to_html(markdown) -> HTMLNode:
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
                html_nodes.append(parent_from_children(tag="p", children=children))
            case BlockType.CODE:
                code_html_node = html_node_from_code_block(block)
                html_nodes.append(ParentNode(tag="pre", children=[code_html_node]))
            case BlockType.QUOTE:
                children = children_html_nodes_from_block(block)
                html_nodes.append(
                    parent_from_children(tag="blockquote", children=children)
                )
            case BlockType.UNORDERED_LIST:
                children = children_text_nodes_from_block(block)
                children = [
                    text_node_to_list_item(child_text_node)
                    for child_text_node in children
                ]
                html_nodes.append(parent_from_children(tag="ul", children=children))
            case BlockType.ORDERED_LIST:
                children = children_text_nodes_from_block(block)
                children = [
                    text_node_to_list_item(child_text_node)
                    for child_text_node in children
                ]
                html_nodes.append(parent_from_children(tag="ol", children=children))
            case BlockType.HEADING:
                text_node = text_to_textnodes(block)[0]
                html_nodes.append(text_node_to_heading_html_node(text_node))

    return ParentNode(tag="div", children=html_nodes)
