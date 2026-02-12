import os
import shutil


# Recursively copies all files and directories from src to dest.
# Creates dest directories as needed; overwrites existing files.
def copy_files_recursive(src_dir_path, dest_dir_path):
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
