from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


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
            if text_node.url == None:
                return LeafNode("a", text_node.text, {"href": "#"})
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url == None:
                return LeafNode("img", "", {"src": "#", "alt": text_node.text})
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"invalid text type: {text_node.text_type}")


def main():
    textnode = TextNode("42", TextType.LINK, "https://boot.dev")
    htmlnode = HTMLNode("p", "text", None, {"class": "main"})
    leafnode = LeafNode("a", "click me", {"href": "https://example.com"})
    print(textnode, "\n")
    print(htmlnode)
    print(leafnode)


if __name__ == "__main__":
    main()
