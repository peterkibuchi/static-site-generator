import unittest
from file_operations import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_trailing_whitespace(self):
        self.assertEqual(extract_title("# Hello   "), "Hello")

    def test_title_with_body(self):
        self.assertEqual(
            extract_title("# Title\n\nSome body text"), "Title")

    def test_single_line_no_newline(self):
        self.assertEqual(extract_title("# Just a heading"), "Just a heading")

    def test_title_with_inline_markdown(self):
        self.assertEqual(
            extract_title("# Hello **world**"), "Hello **world**")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Not an h1")

    def test_no_heading_at_all_raises(self):
        with self.assertRaises(Exception):
            extract_title("Just a paragraph")

    def test_empty_string_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_h1_not_on_first_line_raises(self):
        with self.assertRaises(Exception):
            extract_title("Some text\n# Heading")


if __name__ == "__main__":
    unittest.main()
