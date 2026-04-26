from src.functions.markdown_to_html import markdown_to_html
from src.functions.conversions.markdown_to_nodes import markdown_to_text_nodes
from src.nodes.textnode import TextNode, TextType

from src.utility import logger
from src.utility.logger import get_logger
import unittest


class TestMarkdownToTextNodes(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = get_logger("markdown_to_nodes.log")

    def test_paragraphs(self):
        md = """This is **bolded** paragraph"""

        text_nodes = markdown_to_text_nodes(md, logger=self.logger)
        self.assertListEqual(
            text_nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bolded", text_type=TextType.BOLD),
                TextNode(text=" paragraph", text_type=TextType.TEXT),
            ],
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        text_nodes = markdown_to_text_nodes(md, logger=self.logger)
        self.assertListEqual(
            text_nodes,
            [
                TextNode(text="This is ", text_type=TextType.TEXT),
                TextNode(text="bolded", text_type=TextType.BOLD),
                TextNode(text=" paragraph", text_type=TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
