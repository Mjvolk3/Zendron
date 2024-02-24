import frontmatter


def add_metadata_key(metadata_key: str, file_path: str):
    data = frontmatter.load(file_path)
    data["metadata_key"] = metadata_key
    updated_data = frontmatter.dumps(data)
    with open(file_path, "w") as f:
        f.write(updated_data)


def add_comment_key(comment_key: str, file_path: str):
    data = frontmatter.load(file_path)
    data["comment_key"] = comment_key
    updated_data = frontmatter.dumps(data)
    with open(file_path, "w") as f:
        f.write(updated_data)


def get_updated_time(file_path: str):
    data = frontmatter.load(file_path)
    return data["updated"]
    

def remove_front_matter_keys(keys: list, file_path: str):
    """
    Remove specified keys from the front matter of a markdown file.

    :param keys: A list of keys to be removed from the front matter.
    :param file_path: The path to the markdown file.
    """
    # Load the markdown file
    data = frontmatter.load(file_path)
    
    # Remove specified keys from the front matter
    for key in keys:
        if key in data.metadata:
            del data.metadata[key]
    
    # Dump the updated content back to markdown format
    updated_data = frontmatter.dumps(data)
    
    # Write the updated content back to the file
    with open(file_path, "w") as f:
        f.write(updated_data)

def main():
    pass


if __name__ == "__main__":
    main()
