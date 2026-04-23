from src.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        # only split Text based nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError("you must have matching delimiters")

        # Use even/odd counting to alternate types
        counter = 0
        for section in split_text:
            counter += 1
            if counter % 2 == 1:
                current_type = TextType.TEXT
            else:
                current_type = text_type

            if len(section) == 0:
                continue
            new_nodes.append(TextNode(text=section, text_type=current_type))
    return new_nodes
