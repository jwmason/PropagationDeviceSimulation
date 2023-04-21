from pathlib import Path

def read_input_file_contents(input_file) -> str:
    """Reads the input file and stores it into a string"""
    with open(input_file, "r") as input_file:
        input_str = input_file.readlines()
    return input_str

# Function Not Test Covered:
# Unable to test as the function returns user input,
# which cannot be simulated by unittest
def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    read_contents = read_input_file(input_file_path)
    print(read_contents)


if __name__ == '__main__':
    main()
