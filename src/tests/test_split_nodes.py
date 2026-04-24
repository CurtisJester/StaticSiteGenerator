from src.nodes.textnode import TextNode, TextType
from src.functions.split_nodes_delimiter import split_nodes_delimiter

import unittest


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_split(self):
        old_node = TextNode(
            text="This is a text with a `code block` word.", text_type=TextType.TEXT
        )

        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes[0],
            TextNode(text="This is a text with a ", text_type=TextType.TEXT),
        )
        self.assertEqual(
            new_nodes[1], TextNode(text="code block", text_type=TextType.CODE)
        )
        self.assertEqual(new_nodes[2], TextNode(text=" word.", text_type=TextType.TEXT))

    def test_multi_code_split(self):
        old_node = TextNode(
            text="Twice the `code block`, twice `the fun!`", text_type=TextType.TEXT
        )

        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes[0],
            TextNode(text="Twice the ", text_type=TextType.TEXT),
        )
        self.assertEqual(
            new_nodes[1], TextNode(text="code block", text_type=TextType.CODE)
        )
        self.assertEqual(
            new_nodes[2],
            TextNode(text=", twice ", text_type=TextType.TEXT),
        )
        self.assertEqual(
            new_nodes[3], TextNode(text="the fun!", text_type=TextType.CODE)
        )

    def test_italic_split(self):
        old_node = TextNode(
            text="This is an *italicized word* with padding.", text_type=TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([old_node], "*", text_type=TextType.ITALIC)
        self.assertEqual(
            new_nodes[0], TextNode(text="This is an ", text_type=TextType.TEXT)
        )
        self.assertEqual(
            new_nodes[1], TextNode(text="italicized word", text_type=TextType.ITALIC)
        )
        self.assertEqual(
            new_nodes[2], TextNode(text=" with padding.", text_type=TextType.TEXT)
        )

    def test_multi_node_italic(self):
        old_node = TextNode(
            text="This is an *italicized word* with padding.", text_type=TextType.TEXT
        )
        old_node2 = TextNode(text="Yet more *words*.", text_type=TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            [old_node, old_node2], "*", text_type=TextType.ITALIC
        )
        self.assertEqual(
            new_nodes[0], TextNode(text="This is an ", text_type=TextType.TEXT)
        )
        self.assertEqual(
            new_nodes[1], TextNode(text="italicized word", text_type=TextType.ITALIC)
        )
        self.assertEqual(
            new_nodes[2], TextNode(text=" with padding.", text_type=TextType.TEXT)
        )
        self.assertEqual(
            new_nodes[3], TextNode(text="Yet more ", text_type=TextType.TEXT)
        )
        self.assertEqual(
            new_nodes[4], TextNode(text="words", text_type=TextType.ITALIC)
        )
        self.assertEqual(new_nodes[5], TextNode(text=".", text_type=TextType.TEXT))

    def test_bold_split(self):
        old_node = TextNode(text="Just _words_", text_type=TextType.TEXT)

        new_nodes = split_nodes_delimiter([old_node], "_", text_type=TextType.BOLD)

        self.assertEqual(new_nodes[0], TextNode(text="Just ", text_type=TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode(text="words", text_type=TextType.BOLD))

    def test_odd_delimiters(self):
        old_node = TextNode(
            text="This is an illformed `code block.", text_type=TextType.TEXT
        )

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                old_nodes=[old_node], delimiter="`", text_type=TextType.CODE
            )


if __name__ == "__main__":
    unittest.main()
