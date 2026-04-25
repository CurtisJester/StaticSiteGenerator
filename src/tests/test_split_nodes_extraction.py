from src.functions.split_nodes_extractions import split_nodes_image, split_nodes_link
from src.nodes.textnode import TextNode, TextType

import unittest


class TestSplitNodesExtractions(unittest.TestCase):
    def test_image_split(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_split2(self):
        node = TextNode(
            "This is text with back to back images ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with back to back images ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_link_split(self):
        node = TextNode(
            "[Help](https://boot.dev/help) is available but dont forget your [cats](https://cats.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Help", TextType.LINK, "https://boot.dev/help"),
                TextNode(" is available but dont forget your ", TextType.TEXT),
                TextNode("cats", TextType.LINK, "https://cats.com"),
            ],
            new_nodes,
        )

    def test_link_split2(self):
        node = TextNode(
            "Hello! Here's some [Help](https://boot.dev/help)! Forget your [cats](https://cats.com) for now!!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Hello! Here's some ", TextType.TEXT),
                TextNode("Help", TextType.LINK, "https://boot.dev/help"),
                TextNode("! Forget your ", TextType.TEXT),
                TextNode("cats", TextType.LINK, "https://cats.com"),
                TextNode(" for now!!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_only(self):
        node = TextNode(
            "[Help](https://boot.dev/help)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Help", TextType.LINK, "https://boot.dev/help"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
