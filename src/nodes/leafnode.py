from src.nodes.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("leaf node has no value")
        if not self.tag:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        fmt_str = "LeafNode(Tag={}, Value={}, Props={})"
        return fmt_str.format(self.tag, self.value, self.props)

    def __eq__(self, other) -> bool:
        # Same EQ method as HTMLNode but removes Children check
        if (
            self.tag != other.tag
            or self.value != other.value
            or self.props != other.props
        ):
            return False
        return True
