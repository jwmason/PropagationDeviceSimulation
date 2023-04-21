import unittest
import tempfile
import os
from readinput import read_input_file_contents
from verifycommands import get_commands, verify_commands_length
class TestReadInput(unittest.TestCase):
    """Testing functions in readinput.py"""
    def test_read_input_file(self):
        """Test the storing of input file into a string"""
        input_data = "this is a test\n"
        # This simulates the text file that is being read by the function
        with tempfile.NamedTemporaryFile(mode = "w", delete = False) as temp_file:
            temp_file.write(input_data)
        # Using the function in testing
        output = read_input_file_contents(temp_file.name)
        expected_output = ['this is a test\n']
        temp_file.close()
        # Delete the test file after unittest
        os.remove(temp_file.name)
        self.assertEqual(output, expected_output)
        self.assertEqual(type(output), list)

class TestVerifyCommands(unittest.TestCase):
    """Testing functions in verifycommands.py"""
    def test_get_commands(self):
        """Tests if all possible commands from input file are added
        to the command list returned by the function"""
        input_data = "this is a test\nDEVICE 50\nPROPAGATE\n123LENGTH\n# Hi\n"
        # This simulates the text file that is being read by the function
        with tempfile.NamedTemporaryFile(mode = "w", delete = False) as temp_file:
            temp_file.write(input_data)
        # Using the function in testing
        output = read_input_file_contents(temp_file.name)
        temp_file.close()
        # Delete the test file after unittest
        os.remove(temp_file.name)
        test_cmd_list = get_commands(output)
        expected_cmd_list = ['DEVICE 50\n', 'PROPAGATE\n']
        self.assertEqual(test_cmd_list, expected_cmd_list)

    def test_verify_commands_length(self):
        """Tests if the commands have the correct parameter amounts"""
        input_data = "LENGTH 123\nDEVICE 50\nPROPAGATE\nCANCEL 1 2 3\n"
        # This simulates the text file that is being read by the function
        with tempfile.NamedTemporaryFile(mode = "w", delete = False) as temp_file:
            temp_file.write(input_data)
        # Using the function in testing
        output = read_input_file_contents(temp_file.name)
        temp_file.close()
        # Delete the test file after unittest
        os.remove(temp_file.name)
        test_cmd_list = get_commands(output)
        test_cmd_list = verify_commands_length(test_cmd_list)
        expected_cmd_list = ['LENGTH 123\n', 'DEVICE 50\n', 'CANCEL 1 2 3\n']
        self.assertEqual(test_cmd_list, expected_cmd_list)

if __name__ == '__main__':
    unittest.main()
