"""This module reads the contents of the input file"""

from pathlib import Path


# Function Not Test Covered:
# Unable to test as the function returns user input, which cannot be simulated by unittest
# without downloading a third party library (not in Python Standard Library)
def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def read_input_file_contents(input_file) -> list:
    """Reads the input file and stores it into a list"""
    with open(input_file, "r") as input_file:
        input_list = input_file.readlines()
    return input_list
