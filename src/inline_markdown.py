import re
from typing import Literal

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: Literal["**", "_", "`"],
    text_type: TextType
):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Non-TEXT nodes (e.g. BOLD, LINK) are already typed —
        # pass them through without processing their text
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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Matches ![alt](url) — brackets/parens inside alt or url are excluded
    # to prevent greedy over-matching across multiple images.
    # Returns a list of tuples where each tuple is (alt_text, image_url).
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # Matches [text](url) — the negative lookbehind (?<!!) ensures
    # image syntax ![alt](url) is not matched as a link
    # Returns a list of tuples where each tuple is (anchor_text, link_url).
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Non-TEXT nodes are already typed — pass them through unchanged
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        rest_of_str: str = node.text

        for img_alt, img_url in images:
            # Progressively split the text around each image match,
            # carrying forward the remainder after each split
            parts = rest_of_str.split(f"![{img_alt}]({img_url})", 1)
            left_str, rest_of_str = parts[0], parts[1]

            # Only append TextNodes with text to the final list
            if left_str != "":
                new_nodes.append(TextNode(left_str, TextType.TEXT))
            new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))

        # Append the remaining part after processing all the images, provided it's non-empty
        if rest_of_str != "":
            new_nodes.append(TextNode(rest_of_str, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Non-TEXT nodes are already typed — pass them through unchanged
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        rest_of_str: str = node.text

        for link_text, link_url in links:
            # Progressively split the text around each link match,
            # carrying forward the remainder after each split
            parts = rest_of_str.split(f"[{link_text}]({link_url})", 1)
            left_str, rest_of_str = parts[0], parts[1]

            # Only append TextNodes with text to the final list
            if left_str != "":
                new_nodes.append(TextNode(left_str, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        # Append the remaining part after processing all the images, provided it's non-empty
        if rest_of_str != "":
            new_nodes.append(TextNode(rest_of_str, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str):
    # Process delimiters first so inline formatting inside link/image
    # text (e.g. [**bold**](url)) is resolved before those nodes
    # get locked into LINK/IMAGE types
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
