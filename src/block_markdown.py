def markdown_to_blocks(markdown: str):
    # Split on double newlines to separate blocks (paragraphs, headings, etc.)
    parts = markdown.split("\n\n")
    # Strip leading/trailing whitespace from each block
    stripped = list(map(lambda str: str.strip(), parts))
    # Remove empty blocks caused by extra blank lines
    filtered = list(filter(lambda str: len(str) > 0, stripped))
    return filtered
