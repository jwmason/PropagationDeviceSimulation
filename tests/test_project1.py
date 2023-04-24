"""This module uses unittest to achieve maximum code coverage"""

import unittest

# Import these modules to test read_input_file
# Simulates an input file
import tempfile
import os

# Importing all tested functions
from readinput import read_input_file_contents
from verifycommands import get_commands, verify_commands_length, verify_commands_parameters
from sortcommands import sort_cmd_list

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
        test_input_list = ['this is a test\n', 'DEVICE 50\n', 'PROPAGATE\n', '123LENGTH\n',
                           '# Hi\n', '\n', ' \n', '#\n']
        # Testing function here
        test_cmd_list = get_commands(test_input_list)
        expected_cmd_list = ['DEVICE 50', 'PROPAGATE']
        self.assertEqual(test_cmd_list, expected_cmd_list)

    def test_verify_commands_length(self):
        """Tests if the commands have the correct parameter amounts"""
        test_cmd_list = ['LENGTH 123', 'DEVICE 1 1', 'DEVICE 50', 'DEVICE 12', 'PROPAGATE',
                         'PROPAGATE 1 2 3', 'ALERT 1 2 3', 'ALERT 1 3', 'CANCEL 1 2 3', 'CANCEL 1 2']
        test_cmd_list = get_commands(test_cmd_list)
        # Using the function in testing
        test_cmd_list = verify_commands_length(test_cmd_list)
        expected_cmd_list = ['LENGTH 123', 'DEVICE 50', 'DEVICE 12', 'PROPAGATE 1 2 3',
                             'ALERT 1 2 3', 'CANCEL 1 2 3']
        self.assertEqual(test_cmd_list, expected_cmd_list)

    def test_verify_commands_parameters(self):
        """Tests if the parameters are eligible to be executed"""
        test_cmd_list = ['LENGTH 123', 'DEVICE abc', 'DEVICE -1', 'DEVICE 50', 'DEVICE 12',
                         'PROPAGATE 12 10 10', 'PROPAGATE 1 -1 100',
                         'PROPAGATE a b c', 'PROPAGATE 50 12 10', 'ALERT a b c', 'ALERT 1 ohno 100',
                         'CANCEL -1 nono -1', 'CANCEL 50 testerror 3']
        test_cmd_list = get_commands(test_cmd_list)
        test_cmd_list = verify_commands_length(test_cmd_list)
        # Using the function in testing
        test_cmd_list = verify_commands_parameters(test_cmd_list)
        expected_cmd_list = ['LENGTH 123', 'DEVICE 50', 'DEVICE 12', 'PROPAGATE 50 12 10',
                             'CANCEL 50 testerror 3']
        self.assertEqual(test_cmd_list, expected_cmd_list)


class TestSortCommands(unittest.TestCase):
    """Tests functions in sortcommands.py"""
    def test_sort_cmd_list(self):
        """This tests if the functon sorts set-up commands from 'command' commands"""
        test_cmd_list = ['LENGTH 123', 'DEVICE 50', 'DEVICE 12',
                         'PROPAGATE 50 12 10', 'ALERT 1 ohno 100',
                         'CANCEL 50 testerror 3']
        # Testing function here
        test_set_up, test_command_list = sort_cmd_list(test_cmd_list)
        expected_set_up = ['LENGTH 123', 'DEVICE 50', 'DEVICE 12', 'PROPAGATE 50 12 10']
        expected_command_list = ['ALERT 1 ohno 100', 'CANCEL 50 testerror 3']
        self.assertEqual(test_set_up, expected_set_up)
        self.assertEqual(test_command_list, expected_command_list)

if __name__ == '__main__':
    unittest.main()
