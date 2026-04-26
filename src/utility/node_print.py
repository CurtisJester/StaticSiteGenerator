from src.nodes.textnode import TextType, TextNode
from src.nodes.parentnode import ParentNode
from src.nodes.leafnode import LeafNode


def print_node(node) -> None:
    if isinstance(node, LeafNode):
        print(node)
    else:
        copy = node.copy()
        copy.children = None
        children = node.children
        print(
            f"ParentNode(tag={copy.tag}, value={copy.text}, props={copy.props}, Children: ["
        )
        for child in children:
            print(f"\t{child}")
        print("])")
