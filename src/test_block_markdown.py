import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        result = markdown_to_blocks("hello world")
        self.assertEqual(result, ["hello world"])

    def test_multiple_blocks(self):
        result = markdown_to_blocks("block one\n\nblock two\n\nblock three")
        self.assertEqual(result, ["block one", "block two", "block three"])

    def test_strips_whitespace(self):
        result = markdown_to_blocks("  hello  \n\n  world  ")
        self.assertEqual(result, ["hello", "world"])

    def test_filters_empty_blocks(self):
        result = markdown_to_blocks("hello\n\n\n\nworld")
        self.assertEqual(result, ["hello", "world"])

    def test_multiline_block(self):
        result = markdown_to_blocks("line one\nline two\n\nblock two")
        self.assertEqual(result, ["line one\nline two", "block two"])

    def test_empty_string(self):
        result = markdown_to_blocks("")
        self.assertEqual(result, [])

    def test_only_whitespace(self):
        result = markdown_to_blocks("   \n\n   \n\n   ")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
