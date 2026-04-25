from src.functions.extract_title import extract_title
import unittest


class TestExtractTitle(unittest.TestCase):
    def test_extraction(self):
        md = "# Hello"

        title = extract_title(md)
        self.assertEqual("Hello", title)

    def test_extraction2(self):
        md = "## Hello"
        self.assertRaises(Exception, extract_title, md)

    def test_extraction3(self):
        md = """
# Heading Hello

Now another block of **paragraph** text

Ending here.
"""
        title = extract_title(md)
        self.assertEqual("Heading Hello", title)

    def test_extraction4(self):
        md = ""
        self.assertRaises(Exception, extract_title, md)


if __name__ == "__main__":
    unittest.main()
