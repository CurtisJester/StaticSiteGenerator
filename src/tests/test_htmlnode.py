from src.nodes.htmlnode import HTMLNode


import unittest


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="lorem ipsum")
        node2 = HTMLNode(tag="p", value="lorem ipsum")
        self.assertEqual(node, node2)

    def test_eq2(self):
        child = HTMLNode(tag="h1", value="Title Holder")
        node = HTMLNode(tag="p", value="lorem ipsum", children=[child])
        node2 = HTMLNode(tag="p", value="lorem ipsum", children=[child])
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode(tag="p", value="lorem ipsum")
        node2 = HTMLNode(tag="p", value="another fiction")
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        child = HTMLNode(tag="h1", value="Title Holder")
        node = HTMLNode(tag="body", children=[child])
        node2 = HTMLNode(tag="h2", children=[child])
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="img", props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html2(self):
        node = HTMLNode(
            tag="img", props={"src": "content/img.png", "alt": "alt_text img file"}
        )
        self.assertEqual(
            node.props_to_html(), ' src="content/img.png" alt="alt_text img file"'
        )


if __name__ == "__main__":
    unittest.main()
