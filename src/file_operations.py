import os
import shutil

from block_markdown import markdown_to_html_node


# Recursively copies all files and directories from src to dest.
# Creates dest directories as needed; overwrites existing files.
def copy_files_recursive(src_dir_path: str, dest_dir_path: str):
    print(f"Source: {src_dir_path}, Destination: {dest_dir_path}")

    if not os.path.exists(src_dir_path):
        raise NotADirectoryError(f"{src_dir_path} is not a valid directory")

    # Create the destination directory if it doesn't exist yet;
    # this handles both the top-level call and recursive subdirectory calls
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for path in os.listdir(src_dir_path):
        src_path = os.path.join(src_dir_path, path)
        dest_path = os.path.join(dest_dir_path, path)

        if os.path.isfile(src_path):
            print(f" * {src_path} -> {dest_path}")
            # shutil.copy preserves file content and permissions
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            # Recurse into subdirectory; the next call will create dest_path
            copy_files_recursive(src_path, dest_path)


def extract_title(markdown: str):
    h1 = markdown.split("\n", maxsplit=1)[0]

    if not h1.startswith("# "):
        raise ValueError("All markdown docs must start with an h1")
    return h1[2:].strip()


# Reads a markdown file, converts it to HTML, injects the title and content
# into the template, and writes the final HTML to dest_path.
def generate_page(src_path: str, template_path: str, dest_path: str):
    print(
        f"Generating page from {src_path} to {dest_path} using {template_path}")

    with open(src_path) as src_file:
        markdown = src_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    # Extract the h1 title from raw markdown (before HTML conversion)
    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_str = html_node.to_html()
    # Chain replacements: first inject the title, then the HTML content
    final = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_str)

    # Ensure the destination directory tree exists before writing
    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(final)


# Recursively walks the content directory, converting each .md file
# to an HTML page using the template, mirroring the directory structure in dest.
def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for path in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, path)
        # Swap .md extension to .html for the output filename
        if path.endswith(".md"):
            path = path.removesuffix(".md") + ".html"
        dest_path = os.path.join(dest_dir_path, path)

        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path)
