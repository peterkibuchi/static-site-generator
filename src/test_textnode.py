import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # __init__
    def test_default_url_is_none(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_url_is_set(self):
        node = TextNode("click", TextType.LINK, "https://example.com")
        self.assertEqual(node.url, "https://example.com")

    # __eq__
    def test_eq_same_properties(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("link", TextType.LINK, "https://example.com")
        node2 = TextNode("link", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("link", TextType.LINK, "https://a.com")
        node2 = TextNode("link", TextType.LINK, "https://b.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_none_vs_set(self):
        node = TextNode("link", TextType.LINK)
        node2 = TextNode("link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_eq_non_textnode_returns_false(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertNotEqual(node, "hello")

    # __repr__
    def test_repr_without_url(self):
        node = TextNode("hello", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(hello, text, None)")

    def test_repr_with_url(self):
        node = TextNode("click", TextType.LINK, "https://example.com")
        self.assertEqual(
            repr(node), "TextNode(click, link, https://example.com)")


if __name__ == "__main__":
    unittest.main()
