import os
import os.path as osp
import sys
from dotenv import load_dotenv
load_dotenv()
from os.path import splitext
WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR")
PYTHON_PKG_REL_PATH = os.environ.get("PYTHON_PKG_REL_PATH")
PYTHON_PKG_TEST_REL_PATH = os.environ.get("PYTHON_PKG_TEST_REL_PATH")
GIT_REPO_URL = os.environ.get("GIT_REPO_URL")

def add_frontmatter(file_path):
    # Extract the relative path
    print(f"file path:{file_path}")
    relative_path = osp.relpath(
        file_path, start=WORKSPACE_DIR
    )
    print(f"relative path:{relative_path}")
    # Generate the test file path
    test_file_path = relative_path.replace(PYTHON_PKG_REL_PATH, PYTHON_PKG_TEST_REL_PATH)
    test_file_path = osp.join(
        osp.dirname(test_file_path), "test_" + osp.basename(test_file_path)
    )

    # Generate the frontmatter lines
    # Assuming relative_path contains the file path
    file_extension = splitext(relative_path)[-1]

    # Replace ".py" only if it's the file extension
    if file_extension == ".py":
        relative_path = relative_path.replace('.py', '')

    lines = [
        f"# {relative_path}\n",
        f"# [[{relative_path.replace('/', '.')}]]\n",
        f"# {GIT_REPO_URL}/tree/main/{relative_path}\n",
        f"# Test file: {test_file_path}\n",  # Link to the test file
        "\n",  # Add an extra newline for separation
    ]

    with open(file_path, "r+") as file:
        content = file.readlines()

        print(
            f"Debug: First line of the file: {content[0] if content else 'File is empty'}"
        )

        # Check if frontmatter already exists
        if content and content[0].startswith("# " + relative_path):
            print("Frontmatter already exists.")
            return

        # Add the frontmatter to the content
        content = lines + content
        file.seek(0)
        file.writelines(content)
        file.truncate()  # Ensure any leftover content is removed

    print("Frontmatter added successfully.")


if __name__ == "__main__":
    file_path = sys.argv[1]
    add_frontmatter(file_path)
