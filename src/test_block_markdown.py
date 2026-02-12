import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


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


class TestBlockToBlockType(unittest.TestCase):
    # headings
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type(
            "###### Heading"), BlockType.HEADING)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type(
            "####### Heading"), BlockType.PARAGRAPH)

    # code
    def test_code_block(self):
        self.assertEqual(block_to_block_type(
            "```\nprint('hi')\n```"), BlockType.CODE)

    def test_code_not_closed(self):
        self.assertEqual(block_to_block_type(
            "```\nprint('hi')"), BlockType.PARAGRAPH)

    # quote
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type(
            ">line one\n>line two"), BlockType.QUOTE)

    def test_quote_missing_prefix(self):
        self.assertEqual(block_to_block_type(
            ">line one\nline two"), BlockType.PARAGRAPH)

    # ordered list
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type(
            "1. first\n2. second"), BlockType.ORDERED_LIST)

    def test_ordered_list_no_space(self):
        self.assertEqual(block_to_block_type("1.first"), BlockType.PARAGRAPH)

    # unordered list
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type(
            "- one\n- two"), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        self.assertEqual(block_to_block_type("-one"), BlockType.PARAGRAPH)

    # paragraph
    def test_paragraph(self):
        self.assertEqual(block_to_block_type(
            "just some text"), BlockType.PARAGRAPH)


class TestMarkdownToHTMLNode(unittest.TestCase):
    # paragraph
    def test_paragraph(self):
        result = markdown_to_html_node("hello world").to_html()
        self.assertEqual(result, "<div><p>hello world</p></div>")

    def test_paragraph_with_inline(self):
        result = markdown_to_html_node("hello **bold** world").to_html()
        self.assertEqual(result, "<div><p>hello <b>bold</b> world</p></div>")

    # headings
    def test_heading_h1(self):
        result = markdown_to_html_node("# Hello").to_html()
        self.assertEqual(result, "<div><h1>Hello</h1></div>")

    def test_heading_h3(self):
        result = markdown_to_html_node("### Hello").to_html()
        self.assertEqual(result, "<div><h3>Hello</h3></div>")

    def test_heading_h6(self):
        result = markdown_to_html_node("###### Hello").to_html()
        self.assertEqual(result, "<div><h6>Hello</h6></div>")

    def test_heading_with_inline(self):
        result = markdown_to_html_node("# Hello **bold**").to_html()
        self.assertEqual(result, "<div><h1>Hello <b>bold</b></h1></div>")

    # code
    def test_code_block(self):
        result = markdown_to_html_node("```\nprint('hi')\n```").to_html()
        self.assertEqual(
            result, "<div><pre><code>print('hi')</code></pre></div>")

    # quote
    def test_quote(self):
        result = markdown_to_html_node(">hello world").to_html()
        self.assertEqual(
            result, "<div><blockquote>hello world</blockquote></div>")

    def test_quote_multiline(self):
        result = markdown_to_html_node(">line one\n>line two").to_html()
        self.assertEqual(
            result, "<div><blockquote>line one\nline two</blockquote></div>")

    # ordered list
    def test_ordered_list(self):
        result = markdown_to_html_node("1. first\n2. second").to_html()
        self.assertEqual(
            result, "<div><ol><li>first</li><li>second</li></ol></div>")

    def test_ordered_list_with_inline(self):
        result = markdown_to_html_node("1. **bold**\n2. _italic_").to_html()
        self.assertEqual(
            result, "<div><ol><li><b>bold</b></li><li><i>italic</i></li></ol></div>")

    # unordered list
    def test_unordered_list(self):
        result = markdown_to_html_node("- first\n- second").to_html()
        self.assertEqual(
            result, "<div><ul><li>first</li><li>second</li></ul></div>")

    def test_unordered_list_with_inline(self):
        result = markdown_to_html_node("- **bold**\n- _italic_").to_html()
        self.assertEqual(
            result, "<div><ul><li><b>bold</b></li><li><i>italic</i></li></ul></div>")

    # multiple blocks
    def test_multiple_blocks(self):
        md = "# Heading\n\nparagraph\n\n- one\n- two"
        result = markdown_to_html_node(md).to_html()
        self.assertEqual(
            result,
            "<div><h1>Heading</h1><p>paragraph</p><ul><li>one</li><li>two</li></ul></div>"
        )


if __name__ == "__main__":
    unittest.main()
