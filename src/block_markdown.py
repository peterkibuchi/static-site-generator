import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def markdown_to_blocks(markdown: str):
    # Split on double newlines to separate blocks (paragraphs, headings, etc.)
    parts = markdown.split("\n\n")
    # Strip leading/trailing whitespace from each block
    stripped = list(map(lambda str: str.strip(), parts))
    # Remove empty blocks caused by extra blank lines
    filtered = list(filter(lambda str: len(str) > 0, stripped))
    return filtered


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading: 1 to 6 # characters followed by a space
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING

    # Code: Starts and ends with 3 backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: Every line must start with >
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Ordered List: Every line starts with a number followed by a period and space
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST

    # Unordered List: Every line starts with - followed by a space
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 6. Default: Paragraph
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    child_nodes: list[ParentNode | LeafNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                node = ParentNode("p", text_to_children(block))
                child_nodes.append(node)

            case BlockType.HEADING:
                # Count leading # characters to determine heading level
                level = len(block) - len(block.lstrip("#"))
                text = block[level + 1:]
                node = ParentNode(f"h{level}", text_to_children(text))
                child_nodes.append(node)

            case BlockType.CODE:
                # Strip the opening and closing ``` lines
                inner = block.removeprefix("```").removesuffix("```").strip()
                node = ParentNode("pre", [LeafNode("code", inner)])
                child_nodes.append(node)

            case BlockType.QUOTE:
                lines = block.split("\n")
                content = "\n".join(
                    l.removeprefix(">").lstrip(" ") for l in lines
                )
                node = ParentNode("blockquote", text_to_children(content))
                child_nodes.append(node)

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                # Each line becomes an <li> with its own inline formatting
                new_lines = [re.sub(r"^\d+\.\s", "", l) for l in lines]
                node = ParentNode(
                    "ol", [ParentNode("li", text_to_children(l)) for l in new_lines])
                child_nodes.append(node)

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                # Each line becomes an <li> with its own inline formatting
                new_lines = [l.removeprefix("- ") for l in lines]
                node = ParentNode(
                    "ul", [ParentNode("li", text_to_children(l)) for l in new_lines])
                child_nodes.append(node)

    return ParentNode("div", child_nodes)


def text_to_children(text: str) -> list[ParentNode | LeafNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: list[ParentNode | LeafNode] = list(
        map(text_node_to_html_node, text_nodes)
    )
    return html_nodes
