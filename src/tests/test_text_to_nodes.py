from src.nodes.textnode import TextNode, TextType
from src.functions.node_to_html import text_to_textnodes

import unittest


class TestTextToNode(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertListEqual(text_to_textnodes(text), output)

    def test_text_to_nodes2(self):
        text = "**Bold text** _next to italics_ and then some padding."
        output = [
            TextNode("Bold text", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("next to italics", TextType.ITALIC),
            TextNode(" and then some padding.", TextType.TEXT),
        ]
        self.assertListEqual(text_to_textnodes(text), output)

    def test_text_to_image(self):
        text = "![Bear](https://bear.com/)"
        output = [TextNode("Bear", TextType.IMAGE, "https://bear.com/")]
        self.assertListEqual(text_to_textnodes(text), output)


if __name__ == "__main__":
    unittest.main()
