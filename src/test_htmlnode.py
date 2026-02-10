import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # __init__
    def test_defaults_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_all_properties_set(self):
        child = HTMLNode("span", "child")
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


if __name__ == "__main__":
    unittest.main()
