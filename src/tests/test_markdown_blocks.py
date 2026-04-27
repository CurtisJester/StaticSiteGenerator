from src.functions.markdown_to_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

import unittest


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_heading(self):
        block = "# This is a heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_code(self):
        block = "```\nThis is a code block```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_to_bad_code(self):
        block = "```This is not a code block```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_bad_code2(self):
        block = "```\nThis is a code block but wrong"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_bad_code3(self):
        block = "```This is a code block but wrong\n```"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_quote(self):
        block = "> A quote from above\n>and below"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_to_ordered_list(self):
        block = "1. One of my\n2. Favorite things."
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_bad_ordered_list(self):
        block = "1. One of my\nFavorite things\n2. Is chocolate"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_unordered_list(self):
        block = "- Something\n- New"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_bad_unordered_list(self):
        block = "- Something\nNew\n- I guess"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_paragraph(self):
        block = "This is some lorem ipsum..."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_paragraph_tricky_quote(self):
        block = "This is some \n>lorem ipsum..."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_paragraph_tricky_quote2(self):
        block = ">This is some \nlorem ipsum..."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()
