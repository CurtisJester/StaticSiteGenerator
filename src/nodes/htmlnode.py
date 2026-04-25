class HTMLNode:
    """
    :param tag: The tag with which to surround the HTML node
    :param value: The value of the node, the text inside the tags.
    :param children: The list of children nodes (LeafNodes)
    :param props: The dictionary of props for the HTML Node
    """

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        fmt_str = ""
        if not self.props:
            return fmt_str
        for k, v in self.props.items():
            fmt_str += f' {k}="{v}"'
        return fmt_str

    def __eq__(self, other) -> bool:
        if (
            self.tag != other.tag
            or self.value != other.value
            or self.children != other.children
            or self.props != other.props
        ):
            return False
        return True

    def __repr__(self) -> str:
        fmt_str = "HTMLNode(Tag={}, Value={}, Children=[{}], Props={})"
        return fmt_str.format(self.tag, self.value, self.children, self.props)
