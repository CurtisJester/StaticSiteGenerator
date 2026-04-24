from src.functions.regex_extractions import (
    extract_markdown_images,
    extract_markdown_links,
)

import unittest


class TestRegexExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "My cat ![cat](https://i.imgur.com/cat.png) and my dog ![dog](https://i.imgur.com/dog.jpg)"
        )
        self.assertListEqual(
            [
                ("cat", "https://i.imgur.com/cat.png"),
                ("dog", "https://i.imgur.com/dog.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a link to a [help document](https://pypi.org/)"
        )
        self.assertListEqual([("help document", "https://pypi.org/")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "My [blog](https://nothing-here.com/)!This is a link to a [help document](https://pypi.org/)"
        )
        self.assertListEqual(
            [
                ("blog", "https://nothing-here.com/"),
                ("help document", "https://pypi.org/"),
            ],
            matches,
        )


if __name__ == "__main__":
    unittest.main()
