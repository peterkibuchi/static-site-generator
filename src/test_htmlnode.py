import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # __init__
    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_all_properties_set(self):
        child = LeafNode("span", "child")
        node = HTMLNode("div", "hello", [child], {"class": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"class": "main"})

    # to_html
    def test_to_html_raises(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # props_to_html
    def test_props_to_html_none(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)

    # __repr__
    def test_repr(self):
        node = HTMLNode("p", "hello", None, {"class": "intro"})
        result = repr(node)
        self.assertIn("p", result)
        self.assertIn("hello", result)
        self.assertIn("intro", result)


class TestLeafNode(unittest.TestCase):
    # __init__
    def test_no_children(self):
        node = LeafNode("p", "hello")
        self.assertIsNone(node.children)

    def test_default_props_none(self):
        node = LeafNode("p", "hello")
        self.assertIsNone(node.props)

    def test_props_set(self):
        node = LeafNode("a", "click", {"href": "https://example.com"})
        self.assertEqual(node.props, {"href": "https://example.com"})

    # to_html
    def test_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "hello")
        self.assertEqual(node.to_html(), "<p>hello</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "click", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://example.com">click</a>')

    def test_to_html_no_value_raises(self):
        node = LeafNode("p", None)  # type: ignore
        with self.assertRaises(ValueError):
            node.to_html()

    # __repr__
    def test_repr(self):
        node = LeafNode("p", "hello", {"class": "intro"})
        result = repr(node)
        self.assertIn("p", result)
        self.assertIn("hello", result)
        self.assertIn("intro", result)


class TestParentNode(unittest.TestCase):
    # __init__
    def test_no_value(self):
        node = ParentNode("div", [LeafNode(None, "text")])
        self.assertIsNone(node.value)

    def test_default_props_none(self):
        node = ParentNode("div", [LeafNode(None, "text")])
        self.assertIsNone(node.props)

    def test_children_set(self):
        child = LeafNode("b", "bold")
        node = ParentNode("p", [child])
        self.assertEqual(node.children, [child])

    # to_html
    def test_to_html_single_child(self):
        node = ParentNode("p", [LeafNode("b", "bold")])
        self.assertEqual(node.to_html(), "<p><b>bold</b></p>")

    def test_to_html_multiple_children(self):
        node = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode(None, " normal "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(
            node.to_html(), "<p><b>bold</b> normal <i>italic</i></p>")

    def test_to_html_nested_parent(self):
        inner = ParentNode("span", [LeafNode("b", "bold")])
        outer = ParentNode("div", [inner])
        self.assertEqual(
            outer.to_html(), "<div><span><b>bold</b></span></div>")

    def test_to_html_deeply_nested(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(), "<div><section><p><b>deep</b></p></section></div>")

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode(None, "text")], {
                          "class": "container"})
        self.assertEqual(node.to_html(), '<div class="container">text</div>')

    def test_to_html_no_tag_raises(self):
        node = ParentNode("div", [LeafNode(None, "text")])
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [LeafNode(None, "text")])
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    # __repr__
    def test_repr(self):
        node = ParentNode("div", [LeafNode(None, "text")], {"class": "main"})
        result = repr(node)
        self.assertIn("div", result)
        self.assertIn("main", result)


if __name__ == "__main__":
    unittest.main()
