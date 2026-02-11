import re
from enum import Enum


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
