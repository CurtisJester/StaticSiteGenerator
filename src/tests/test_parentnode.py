from src.nodes.parentnode import ParentNode
from src.nodes.leafnode import LeafNode

import unittest


class TestParentNode(unittest.TestCase):
    def __init__(self, method_name: str) -> None:
        super().__init__(method_name)
        self.child_node1 = LeafNode("b", "Bold text")
        self.child_node2 = LeafNode(None, "Normal text")
        self.child_node3 = LeafNode("i", "Italic text")

        self.parent_node = ParentNode("h1", children=[self.child_node1])
        self.parent_node2 = ParentNode(
            "p", children=[self.parent_node, self.child_node3]
        )

    def test_eq(self):
        node = ParentNode(tag="p", children=[self.child_node1, self.child_node2])
        node2 = ParentNode(tag="p", children=[self.child_node1, self.child_node2])
        self.assertEqual(node, node2)

    def test_neq(self):
        node = ParentNode(tag="p", children=[self.child_node1, self.child_node2])
        node2 = ParentNode(tag="h1", children=[self.child_node3, self.child_node2])
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = ParentNode(tag="p", children=[self.child_node2])
        node2 = ParentNode(tag="p", children=[self.child_node3, self.child_node2])
        self.assertNotEqual(node, node2)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_nested_to_html(self):
        self.assertEqual(
            self.parent_node2.to_html(),
            "<p><h1><b>Bold text</b></h1><i>Italic text</i></p>",
        )


if __name__ == "__main__":
    unittest.main()
