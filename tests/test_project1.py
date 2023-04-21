import unittest
import tempfile
import os
from pathlib import Path
from project1 import read_input_file_contents, _read_input_file_path
class TestProject1(unittest.TestCase):
    """Testing all functions in project1.py"""
    def test_read_input_file(self):
        """Test the storing of input file into a string"""
        input_data = "this is a test\n"
        # This simulates the text file that is being read by the function
        with tempfile.NamedTemporaryFile(mode = "w", delete = False) as temp_file:
            temp_file.write(input_data)
        output = read_input_file_contents(temp_file.name)
        expected_output = ['this is a test\n']
        temp_file.close()
        # Delete the test file after unittest
        os.remove(temp_file.name)
        self.assertEqual(output, expected_output)
