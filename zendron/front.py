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


def main():
    pass


if __name__ == "__main__":
    main()
