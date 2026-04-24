from src.nodes.leafnode import LeafNode

import unittest


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a text")
        node2 = LeafNode("p", "This is a text")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = LeafNode("h1", "Title Text")
        node2 = LeafNode("h1", "Title Text")
        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Huzzah!")
        self.assertEqual(node.to_html(), "<h1>Huzzah!</h1>")


if __name__ == "__main__":
    unittest.main()
