import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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


class TestSplitNodesDelimiter(unittest.TestCase):
    # basic splitting
    def test_bold(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello **world** bye", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" bye", TextType.TEXT),
        ])

    def test_italic(self):
        nodes = split_nodes_delimiter(
            [TextNode("hello _world_ bye", TextType.TEXT)], "_", TextType.ITALIC)
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.ITALIC),
            TextNode(" bye", TextType.TEXT),
        ])

    def test_code(self):
        nodes = split_nodes_delimiter(
            [TextNode("use `print()` here", TextType.TEXT)], "`", TextType.CODE)
        self.assertEqual(nodes, [
            TextNode("use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    # edge cases
    def test_delimiter_at_start(self):
        nodes = split_nodes_delimiter(
            [TextNode("**bold** text", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        nodes = split_nodes_delimiter(
            [TextNode("text **bold**", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])

    def test_multiple_delimited_sections(self):
        nodes = split_nodes_delimiter(
            [TextNode("a **b** c **d** e", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.TEXT),
        ])

    def test_no_delimiter(self):
        nodes = split_nodes_delimiter(
            [TextNode("plain text", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(nodes, [TextNode("plain text", TextType.TEXT)])

    # non-TEXT nodes pass through unchanged
    def test_non_text_node_passthrough(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(nodes, [bold_node])

    def test_mixed_text_and_non_text(self):
        nodes = split_nodes_delimiter([
            TextNode("hello **world**", TextType.TEXT),
            TextNode("link", TextType.LINK),
        ], "**", TextType.BOLD)
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("link", TextType.LINK),
        ])

    # error case
    def test_unmatched_delimiter_raises(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("hello **world", TextType.TEXT)], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        result = extract_markdown_images("![alt](https://example.com/img.png)")
        self.assertEqual(result, [("alt", "https://example.com/img.png")])

    def test_multiple_images(self):
        result = extract_markdown_images(
            "![one](https://a.com/1.png) and ![two](https://b.com/2.png)")
        self.assertEqual(result, [
            ("one", "https://a.com/1.png"),
            ("two", "https://b.com/2.png"),
        ])

    def test_no_images(self):
        result = extract_markdown_images("just plain text")
        self.assertEqual(result, [])

    def test_does_not_match_links(self):
        result = extract_markdown_images("[click](https://example.com)")
        self.assertEqual(result, [])

    def test_empty_alt(self):
        result = extract_markdown_images("![](https://example.com/img.png)")
        self.assertEqual(result, [("", "https://example.com/img.png")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        result = extract_markdown_links("[click](https://example.com)")
        self.assertEqual(result, [("click", "https://example.com")])

    def test_multiple_links(self):
        result = extract_markdown_links(
            "[one](https://a.com) and [two](https://b.com)")
        self.assertEqual(result, [
            ("one", "https://a.com"),
            ("two", "https://b.com"),
        ])

    def test_no_links(self):
        result = extract_markdown_links("just plain text")
        self.assertEqual(result, [])

    def test_does_not_match_images(self):
        result = extract_markdown_links("![alt](https://example.com/img.png)")
        self.assertEqual(result, [])

    def test_link_and_image_mixed(self):
        result = extract_markdown_links(
            "[click](https://a.com) and ![alt](https://b.com/img.png)")
        self.assertEqual(result, [("click", "https://a.com")])

    def test_empty_text(self):
        result = extract_markdown_links("[](https://example.com)")
        self.assertEqual(result, [("", "https://example.com")])


if __name__ == "__main__":
    unittest.main()
