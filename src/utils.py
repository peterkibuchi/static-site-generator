from typing import Literal

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            # Fall back to "#" if no URL provided
            if text_node.url == None:
                return LeafNode("a", text_node.text, {"href": "#"})
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            # Fall back to "#" if no URL; value is empty since
            # img tags render via src/alt attributes, not inner text
            if text_node.url == None:
                return LeafNode("img", "", {"src": "#", "alt": text_node.text})
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: Literal["**", "_", "`"],
    text_type: TextType
):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        # Splitting by the delimiter produces alternating segments:
        # even-indexed = plain text, odd-indexed = delimited text.
        # e.g. "hello **world** bye".split("**") -> ["hello ", "world", " bye"]
        # An even number of parts means an unmatched delimiter.
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(
                f"invalid markdown: {delimiter} must have a corresponding closing {delimiter}")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes
