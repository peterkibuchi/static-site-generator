from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def main():
    textnode = TextNode("42", TextType.LINK, "https://boot.dev")
    htmlnode = HTMLNode("p", "text", None, {"class": "main"})
    leafnode = LeafNode("a", "click me", {"href": "https://example.com"})
    print(textnode, "\n")
    print(htmlnode)
    print(leafnode)


if __name__ == "__main__":
    main()
