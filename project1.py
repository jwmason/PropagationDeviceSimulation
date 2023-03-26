from pathlib import Path


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()


if __name__ == '__main__':
    main()
