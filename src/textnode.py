from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: str | None = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    # Accepts `object` to match the base class signature;
    # gracefully returns False for non-TextNode comparisons
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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
