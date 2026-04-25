from src.functions.regex_extractions import (
    extract_markdown_images,
    extract_markdown_links,
)
from src.nodes.textnode import TextNode, TextType


def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        # We do not care about non-text nodes (they have already been formatted)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text_window = old_node.text

        for img_alt_text, img_src in extract_markdown_images(old_node.text):
            sections = text_window.split(f"![{img_alt_text}]({img_src})", 1)

            # TextNode the before
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))

            # Update remaining text
            text_window = sections[1]

            # add Link
            new_nodes.append(
                TextNode(text=img_alt_text, text_type=TextType.IMAGE, url=img_src)
            )

        # Any remaining text is added
        if text_window:
            new_nodes.append(TextNode(text=text_window, text_type=TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        # We do not care about non-text nodes (they have already been formatted)
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text_window = old_node.text

        for link_text, link_url in extract_markdown_links(old_node.text):
            sections = text_window.split(f"[{link_text}]({link_url})", 1)
            # TextNode the before
            if sections[0] != "":
                new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))

            # Update remaining text
            text_window = sections[1]

            # add Link
            new_nodes.append(
                TextNode(text=link_text, text_type=TextType.LINK, url=link_url)
            )

        # Any remaining text is added
        if text_window:
            new_nodes.append(TextNode(text=text_window, text_type=TextType.TEXT))

    return new_nodes
