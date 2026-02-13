import os
import shutil
import sys

from file_operations import copy_files_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"  # use "./public" for local testing
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Optional CLI arg for URL base path (e.g. "/repo-name/" for GitHub Pages)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
