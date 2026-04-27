from src.nodes.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("leaf node has no value")
        if not self.tag:
            return self.value

        props_str = ""
        if self.props:
            props_str += " "
            for k, v in self.props.items():
                props_str += f'{k}="{v}" '
            props_str = props_str.rstrip()

        if self.tag == "img":
            return f"<{self.tag}{props_str}>"
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        fmt_str = "LeafNode(Tag={}, Value={}, Props={})"
        return fmt_str.format(self.tag, self.value, self.props)

    def __eq__(self, other) -> bool:
        if (
            self.tag != other.tag
            or self.value != other.value
            or self.props != other.props
        ):
            return False
        return True
