from typing import Text
import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    ## Tests relate to the TextNode class ##
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("image alt text", TextType.IMAGE, "content/img1.png")
        node2 = TextNode("image alt text", TextType.IMAGE, "content/img1.png")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode(
            "This is some achor text", TextType.LINK, "https://www.boot.dev"
        )
        node2 = TextNode("Nothing here", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_same_text(self):
        node = TextNode("abcd", TextType.CODE)
        node2 = TextNode("abcd", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_same_type(self):
        node = TextNode("zyxv", TextType.ITALIC)
        node2 = TextNode("abcd", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    ## Tests relate to the text_node_to_html_node() function ##
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_img(self):
        node = TextNode("img alt text", TextType.IMAGE, url="content/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)

        correct_props = {"src": "content/img.png", "alt": "img alt text"}
        self.assertEqual(html_node.props, correct_props)

    def test_code(self):
        node = TextNode('print("Hello, world!")', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, 'print("Hello, world!")')


if __name__ == "__main__":
    unittest.main()
