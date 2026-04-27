from src.nodes.textnode import TextType, TextNode
from src.nodes.parentnode import ParentNode
from src.nodes.leafnode import LeafNode

from src.functions.split_nodes_extractions import split_nodes_image, split_nodes_link
from src.functions.split_nodes_delimiter import split_nodes_delimiter


def parent_node_from_children_nodes(tag: str, children: list[LeafNode], props=None):
    """
    Given a tag, props, and a list of children, return a ParentNode
    """
    return ParentNode(tag=tag, children=children, props=props)


def text_to_children(text) -> list[LeafNode]:
    """
    Given a text, process inline Markdown and translate each node into HTML Nodes
    """
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        leafnode = text_node_to_html_node(text_node)
        html_nodes.append(leafnode)

    return html_nodes


def text_to_textnodes(text) -> list[TextNode]:
    """
    Given a line of text, split it into a list of TextNodes that apply
    the correct Type based on the delimiters for inline Markdown.
    """
    original_nodes = [TextNode(text=text, text_type=TextType.TEXT)]

    # delimiter, TYPE pairs
    mappings = {
        "`": TextType.CODE,
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
    }

    new_nodes = original_nodes

    # For delimiter and Text Type, update nodes
    for delimiter, text_type in mappings.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type=text_type)

    # For image and links, update nodes
    for func in [split_nodes_image, split_nodes_link]:
        new_nodes = func(new_nodes)

    return new_nodes


def text_node_to_heading_html_node(text_node: TextNode) -> LeafNode:
    """
    Given a TextNode representing a Header, return a LeafNode that contains
    the correct tag (h1, ... h6) depending on the number of # symbols seen.
    """
    tag = "h{}"

    heading_num = text_node.text.count("#")
    heading_str = text_node.text.split(" ", 1)[1].strip()

    if heading_num < 1 or heading_num > 6:
        raise ValueError(f"Cannot format Heading with len of {heading_num}")
    tag = tag.format(str(heading_num))
    return LeafNode(tag=tag, value=heading_str)


def text_node_to_list_item(text_node: TextNode) -> LeafNode:
    """
    Given a TextNode return a LeafNode with the List tag
    """
    return LeafNode(tag="li", value=text_node.text)


def text_nodes_to_list_item(text_nodes: list[TextNode]) -> ParentNode:
    """
    Given a list of text nodes, separate them by a space and create a single
    LeafNode
    """
    leaf_nodes = []
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return ParentNode(tag="li", children=leaf_nodes)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Given a TextNode return a LeafNode based on the type.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            local_text = text_node.text.strip()
            if local_text.startswith("```\n"):
                local_text = local_text.replace("```\n", "")
                local_text = local_text.replace("```", "")
            return LeafNode(tag="code", value=local_text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value=text_node.text,
                props={"src": text_node.url, "alt": text_node.text},
            )
