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
    parent_node_from_children_nodes,
    text_node_to_heading_html_node,
    text_node_to_list_item,
    text_node_to_html_node,
    text_nodes_to_list_item,
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


def html_node_from_quote(block) -> ParentNode:
    """
    Given a block (a single/multiline str) of quote text, return a list of TextNodes
    after applying inline Markdown
    """
    full_text = ""
    for line in block.split("\n"):
        fixed_line = line[2:] if line.startswith("> ") else line[1:]
        full_text += fixed_line + " "
    full_text = full_text.rstrip()

    text_nodes = text_to_textnodes(full_text)
    children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return ParentNode(tag="blockquote", children=children)


def list_block_to_parent_html_node(block, list_type: BlockType) -> ParentNode:
    list_item_nodes = []

    for line in block.split("\n"):
        fixed_line = line

        # Fix line by type
        if list_type == BlockType.ORDERED_LIST:
            tokens = fixed_line.split(" ")
            # This should remove the '1. ' -> '999. ' etc,
            fixed_line = "".join(tokens[1:])
        if list_type == BlockType.UNORDERED_LIST:
            fixed_line = fixed_line[1:]
            if fixed_line.startswith(" "):
                fixed_line = fixed_line[1:]
        print("DEBUG == Line to Fixed_line == ", line, "==>", fixed_line)
        line_text_nodes = text_to_textnodes(fixed_line)
        list_item_nodes.append(text_nodes_to_list_item(line_text_nodes))

    parent_tag = "ul" if list_type == BlockType.UNORDERED_LIST else "ol"
    return ParentNode(tag=parent_tag, children=list_item_nodes)


def markdown_to_html(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_type_pairs = []
    for block in blocks:
        block_type_pairs.append((block_to_block_type(block), block))

    html_nodes = []
    for block_type, block in block_type_pairs:
        if len(block) == 0:
            continue

        print(block, " ==> DEBUG ==> ", block_type)
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
                html_nodes.append(html_node_from_quote(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(
                    list_block_to_parent_html_node(block, BlockType.UNORDERED_LIST)
                )
            case BlockType.ORDERED_LIST:
                html_nodes.append(
                    list_block_to_parent_html_node(block, BlockType.ORDERED_LIST)
                )
            case BlockType.HEADING:
                text_node = text_to_textnodes(block)[0]
                html_nodes.append(text_node_to_heading_html_node(text_node))

    return ParentNode(tag="div", children=html_nodes)
