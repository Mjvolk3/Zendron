import os
import sys
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR")
VSCODE_PATH = os.environ.get("VSCODE_PATH")


def convert_to_dendron_path(file_path):
    """Convert a file path to Dendron's period-delimited format."""
    # Remove the leading path to the workspace
    relative_path = file_path.replace(
        WORKSPACE_DIR, ""
    )
    dendron_path = relative_path.replace("/", ".").replace(".py", "")
    return dendron_path


def open_related_files(src_file_path):
    # Get the dendron path for the related markdown file
    print("src_file_path ", src_file_path)
    dendron_path = convert_to_dendron_path(src_file_path)[1:]
    print("dendron_path: ", dendron_path)
    md_file_path = os.path.join(
        WORKSPACE_DIR, "notes", dendron_path + ".md"
    )
    print(md_file_path)

    # Construct the test file path
    dir_path, filename = os.path.split(src_file_path)
    test_filename = "test_" + filename
    test_file_path = os.path.join(dir_path.replace("src", "tests"), test_filename)
    print(test_file_path)
    # Check if the markdown file exists
    print(f"md_file_path: {md_file_path}")
    if os.path.exists(md_file_path):
        print("md exists")
        subprocess.run(
            [VSCODE_PATH, md_file_path]
        )  # Open the markdown file in VSCode

    # Check if the test file exists
    print(f"test_file_path: {test_file_path}")
    if os.path.exists(test_file_path):
        print("test exists")
        subprocess.run(
            [VSCODE_PATH, test_file_path]
        )  # Open the test file in VSCode

    # Add a delay to ensure files are opened before the prompt
    time.sleep(2)

    # Ask for user confirmation to delete the source file
    confirm = input(
        f"Do you want to delete the source file {src_file_path}? (yes/no): "
    )
    if confirm.lower() == "yes":
        if os.path.exists(src_file_path):
            os.remove(src_file_path)
        print("Src File deleted.")
    else:
        print("Deletion cancelled.")


if __name__ == "__main__":
    src_file_path = sys.argv[1]
    open_related_files(src_file_path)
