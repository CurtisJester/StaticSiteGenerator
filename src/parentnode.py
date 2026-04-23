from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def __eq__(self, other) -> bool:
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
        if self.children == []:
            raise ValueError("parent cannot have zero children")
        fmt_str = "<{tag}>{children_vals}</{tag}>"
        children_repr = ""
        for child in self.children:
            children_repr += child.to_html()

        return fmt_str.format(tag=self.tag, children_vals=children_repr)
