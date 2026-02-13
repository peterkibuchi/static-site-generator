# Static Site Generator

This is a custom-built static site generator written in Python. It transforms Markdown content into a fully functional HTML website using a template system.

## Overview

The generator processes a directory of Markdown files, converts the content to HTML, and organizes the resulting files based on a provided template. It also manages static assets like CSS and images, ensuring they are correctly copied to the output directory.

## Features

- **Markdown to HTML Conversion:** Supports various Markdown elements including headers, bold text, italics, code blocks, and links.
- **Recursive Directory Processing:** Automatically crawls a content directory to generate pages for all Markdown files found.
- **Static Asset Management:** Copies CSS, images, and other static files from a source directory to the destination.
- **Template System:** Uses a base HTML template to ensure a consistent look and feel across all generated pages.
- **Clean Builds:** Wipes the destination directory before each build to ensure no stale files remain.

## Project Structure

- `src/`: Contains the Python source code for the generator.
- `static/`: The directory for static assets (CSS, images, etc.).
- `content/`: Where the Markdown content files are stored.
- `template.html`: The base HTML structure for the site.
- `docs/`: The output directory where the generated site is built. Use `public/` for local development and testing.

## Getting Started

### Prerequisites

This project uses `uv` for dependency management. If you do not have it installed, follow the [official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Setup and Execution

1. Initialize the virtual environment and activate it:

   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. To generate the static site, run the following command:

   ```bash
   ./main.sh
   ```

The resulting website will be generated in the public/ directory.

## Technical Details

The project utilizes a custom-built Markdown parser that processes text into blocks (paragraphs, headings, lists) and subsequently into inline nodes (bold, italic, links). This hierarchical approach ensures robust and predictable HTML generation while maintaining high extensibility for future Markdown features.
