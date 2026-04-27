from re import A
from src.nodes.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def __eq__(self, other) -> bool:
        if type(other) is list:
            print("Other: ", other)
        if (
            self.tag != other.tag
            or self.children != other.children
            or self.props != other.props
        ):
            return False
        return True

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node has no tag")
        if not self.children:
            raise ValueError(f"parent (tag={self.tag}) cannot have zero children")
        props_str = ""
        if self.props:
            props_str += " "
            for k, v in self.props.items():
                props_str += f'{k}="{v}" '
            props_str = props_str.rstrip()

        fmt_str = "<{tag}{props_str}>{children_vals}</{tag}>"
        children_repr = ""
        for child in self.children:
            children_repr += child.to_html()

        return fmt_str.format(
            tag=self.tag, props_str=props_str, children_vals=children_repr
        )
