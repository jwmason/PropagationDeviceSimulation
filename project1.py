"""This module runs the program"""

from readinput import _read_input_file_path, read_input_file_contents

def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    read_contents = read_input_file_contents(input_file_path)
    print(read_contents)


if __name__ == '__main__':
    main()
