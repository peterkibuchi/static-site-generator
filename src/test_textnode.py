import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = text_node_to_html_node(TextNode("hello", TextType.TEXT))
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "hello")

    def test_bold(self):
        node = text_node_to_html_node(TextNode("bold", TextType.BOLD))
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "bold")

    def test_italic(self):
        node = text_node_to_html_node(TextNode("italic", TextType.ITALIC))
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "italic")

    def test_code(self):
        node = text_node_to_html_node(TextNode("print()", TextType.CODE))
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "print()")

    def test_link(self):
        node = text_node_to_html_node(
            TextNode("click", TextType.LINK, "https://example.com"))
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "click")
        self.assertEqual(node.props, {"href": "https://example.com"})

    def test_link_no_url(self):
        node = text_node_to_html_node(TextNode("click", TextType.LINK))
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "click")
        self.assertEqual(node.props, {"href": "#"})

    def test_image(self):
        node = text_node_to_html_node(
            TextNode("alt text", TextType.IMAGE, "https://example.com/img.png"))
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {
            "src": "https://example.com/img.png",
            "alt": "alt text",
        })

    def test_image_no_url(self):
        node = text_node_to_html_node(TextNode("alt text", TextType.IMAGE))
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertEqual(node.props, {"src": "#", "alt": "alt text"})

    def test_invalid_type_raises(self):
        node = TextNode("hello", TextType.TEXT)
        node.text_type = "invalid"  # type: ignore
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_returns_leafnode(self):
        node = text_node_to_html_node(TextNode("hello", TextType.TEXT))
        self.assertIsInstance(node, LeafNode)


if __name__ == "__main__":
    unittest.main()
