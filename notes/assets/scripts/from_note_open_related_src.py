# /Users/michaelvolk/Documents/projects/torchcell/notes/assets/scripts/from_note_open_related_src.py
import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR")
VSCODE_PATH = os.environ.get("VSCODE_PATH")


def convert_to_file_path(dendron_path):
    """Convert Dendron's period-delimited format to a file path."""
    # Append the leading path to the workspace
    return os.path.join(WORKSPACE_DIR, dendron_path.replace(".", "/") + ".py")


def open_related_src_file(note_file_path):
    print("note_file_path ", note_file_path)

    # Extract the dendron path from the note file path
    dendron_path = (
        note_file_path.replace(WORKSPACE_DIR, "")
        .replace("notes", "")
        .replace(".md", "")
        .lstrip("/")
        .lstrip("\\")
    )
    print("dendron_path: ", dendron_path)

    src_file_path = convert_to_file_path(dendron_path)
    print("src_file_path: ", src_file_path)

    if os.path.exists(src_file_path):
        print("src exists")
        subprocess.run(
            [VSCODE_PATH, src_file_path]
        )  # Open the related src file in VSCode


if __name__ == "__main__":
    note_file_path = sys.argv[1]
    open_related_src_file(note_file_path)
