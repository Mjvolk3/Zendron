import os
import sys
import subprocess
from dotenv import load_dotenv
from pathlib import Path

# Load the environment variables
load_dotenv()

# Get the environment variables
PYTHON_PKG_REL_PATH = os.getenv("PYTHON_PKG_REL_PATH")
PYTHON_PKG_TEST_REL_PATH = os.getenv("PYTHON_PKG_TEST_REL_PATH")
VSCODE_PATH = os.getenv("VSCODE_PATH")
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR")


def create_test_file(src_file_path):
    print('=' * 80)
    # Get the relative path from the source directory to WORKSPACE_DIR
    rel_path_from_workspace_to_src_file = os.path.relpath(src_file_path, WORKSPACE_DIR)

    print(
        f"Relative path from workspace to source file: {rel_path_from_workspace_to_src_file}"
    )

    # Form new path using PYTHON_PKG_TEST_REL_PATH
    test_file_relative_path = rel_path_from_workspace_to_src_file.replace(PYTHON_PKG_REL_PATH, PYTHON_PKG_TEST_REL_PATH)

    # Construct the full path of the test file
    test_file_path = os.path.join(WORKSPACE_DIR, test_file_relative_path)
    test_file_directory = os.path.dirname(test_file_path)
    test_filename = "test_" + os.path.basename(src_file_path)
    test_file_path = os.path.join(test_file_directory, test_filename)

    print(f"Test file path: {test_file_path}")

    # If the test file doesn't exist, create it
    if not os.path.exists(test_file_path):
        os.makedirs(test_file_directory, exist_ok=True)
        with open(test_file_path, "w") as test_file:
            test_file.write("# Test file\n")
        print(f"Test file created at: {test_file_path}")
    else:
        print(f"Test file already exists at: {test_file_path}")

    # Open the test file in VSCode
    subprocess.run([VSCODE_PATH, test_file_path])
    print('=' * 80)

if __name__ == "__main__":
    event = sys.argv[1]
    src_file_path = sys.argv[2]

    if event == "create":
        create_test_file(src_file_path)
