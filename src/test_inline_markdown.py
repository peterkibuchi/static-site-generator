import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = split_nodes_image(
            [TextNode("text ![alt](https://example.com/img.png) more", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("text ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" more", TextType.TEXT),
        ])

    def test_image_at_start(self):
        nodes = split_nodes_image(
            [TextNode("![alt](https://example.com/img.png) after", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_image_at_end(self):
        nodes = split_nodes_image(
            [TextNode("before ![alt](https://example.com/img.png)", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
        ])

    def test_multiple_images(self):
        nodes = split_nodes_image(
            [TextNode("![a](https://a.com) mid ![b](https://b.com)", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("a", TextType.IMAGE, "https://a.com"),
            TextNode(" mid ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "https://b.com"),
        ])

    def test_no_images(self):
        nodes = split_nodes_image([TextNode("plain text", TextType.TEXT)])
        self.assertEqual(nodes, [TextNode("plain text", TextType.TEXT)])

    def test_non_text_passthrough(self):
        node = TextNode("bold", TextType.BOLD)
        nodes = split_nodes_image([node])
        self.assertEqual(nodes, [node])

    def test_mixed_text_and_non_text(self):
        nodes = split_nodes_image([
            TextNode("see ![img](https://a.com)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])
        self.assertEqual(nodes, [
            TextNode("see ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://a.com"),
            TextNode("bold", TextType.BOLD),
        ])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = split_nodes_link(
            [TextNode("text [click](https://example.com) more", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("text ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" more", TextType.TEXT),
        ])

    def test_link_at_start(self):
        nodes = split_nodes_link(
            [TextNode("[click](https://example.com) after", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_link_at_end(self):
        nodes = split_nodes_link(
            [TextNode("before [click](https://example.com)", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://example.com"),
        ])

    def test_multiple_links(self):
        nodes = split_nodes_link(
            [TextNode("[a](https://a.com) mid [b](https://b.com)", TextType.TEXT)])
        self.assertEqual(nodes, [
            TextNode("a", TextType.LINK, "https://a.com"),
            TextNode(" mid ", TextType.TEXT),
            TextNode("b", TextType.LINK, "https://b.com"),
        ])

    def test_no_links(self):
        nodes = split_nodes_link([TextNode("plain text", TextType.TEXT)])
        self.assertEqual(nodes, [TextNode("plain text", TextType.TEXT)])

    def test_non_text_passthrough(self):
        node = TextNode("bold", TextType.BOLD)
        nodes = split_nodes_link([node])
        self.assertEqual(nodes, [node])

    def test_mixed_text_and_non_text(self):
        nodes = split_nodes_link([
            TextNode("see [click](https://a.com)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ])
        self.assertEqual(nodes, [
            TextNode("see ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://a.com"),
            TextNode("bold", TextType.BOLD),
        ])


class TestTextToTextnodes(unittest.TestCase):
    def test_plain_text(self):
        nodes = text_to_textnodes("just plain text")
        self.assertEqual(nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_bold(self):
        nodes = text_to_textnodes("hello **bold** world")
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT),
        ])

    def test_italic(self):
        nodes = text_to_textnodes("hello _italic_ world")
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", TextType.TEXT),
        ])

    def test_code(self):
        nodes = text_to_textnodes("hello `code` world")
        self.assertEqual(nodes, [
            TextNode("hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT),
        ])

    def test_image(self):
        nodes = text_to_textnodes("see ![alt](https://img.com/a.png) here")
        self.assertEqual(nodes, [
            TextNode("see ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_link(self):
        nodes = text_to_textnodes("see [click](https://example.com) here")
        self.assertEqual(nodes, [
            TextNode("see ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_all_types(self):
        text = "This is **bold** and _italic_ and `code` and ![img](https://i.com/a.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://i.com/a.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ])


if __name__ == "__main__":
    unittest.main()
