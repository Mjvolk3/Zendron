from datetime import datetime
from typing import Union


def utc_parse(date_string):
    # substitute Z with +00:00 for proper UTC formatting. Z stands for 0 offset.
    if date_string == "":
        return None
    if date_string[-1] == "Z":
        date_string = date_string[:-1] + "+00:00"
    return datetime.fromisoformat(date_string)


def main():
    pass


if __name__ == "__main__":
    main()
