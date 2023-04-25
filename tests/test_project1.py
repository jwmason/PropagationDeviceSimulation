"""This module uses unittest to achieve maximum code coverage"""

import unittest

# Import these modules to test read_input_file
# Simulates an input file
import tempfile
import os

# Import these modules to test print output
import contextlib
import io

# Importing all tested functions
from readinput import read_input_file_contents
from verifycommands import get_commands, verify_commands_length, verify_commands_parameters
from sortcommands import sort_cmd_list, sort_set_up_list, sort_command_list
from runcommands import run_set_up_commands, run_command_commands
from devices import Device

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

    def test_sort_set_up_list(self):
        """This tests if the function properly sorts the device and set-up lists"""
        test_set_up = ['PROPAGATE 50 12 10', 'LENGTH 123', 'DEVICE 50', 'DEVICE 12']
        # Testing function here
        devices_list, set_up_list = sort_set_up_list(test_set_up)
        expected_devices_list = ['DEVICE 50', 'DEVICE 12']
        expected_set_up_list = ['PROPAGATE 50 12 10', 'LENGTH 123']
        self.assertEqual(devices_list, expected_devices_list)
        self.assertEqual(set_up_list, expected_set_up_list)

    def test_sort_command_list(self):
        """This tests if function properly sorts the command list"""
        test_command = ['ALERT 1 ohno 100', 'CANCEL 50 testerror 3', 'CANCEL 3 test 55']
        # Testing function here
        command_list = sort_command_list(test_command)
        expected_command_list = ['CANCEL 50 testerror 3', 'CANCEL 3 test 55', 'ALERT 1 ohno 100']
        self.assertEqual(command_list, expected_command_list)

class TestRunCommands(unittest.TestCase):
    """This tests functions within runcommands.py"""
    def test_set_up_commands(self):
        """Tests if set-up commands are run correctly"""
        test_set_up = ['PROPAGATE 50 12 10', 'LENGTH 123', 'DEVICE 50', 'DEVICE 12']
        # Testing function
        test_device = run_set_up_commands(test_set_up)
        self.assertEqual(test_device.length, 123)
        self.assertEqual(test_device.device_number_list, [50, 12])
        self.assertEqual(test_device.propagate, [[50, 12, 10]])

    def test_run_command_commands(self):
        """Tests if 'command' commands are run correctly"""
        test_command_list = ['ALERT 50 ohno 0', 'CANCEL 50 testerror 200']
        test_device = Device()
        test_device.length = 500
        test_device.device_id = [50, 12]
        test_device.propagate.append([12, 10])
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run_command_commands(test_command_list, test_device)
        expected_output = '@0: #50 SENT ALERT TO #12: ohno\n' \
                          '@10: #12 RECEIVED ALERT FROM #50: ohno\n' \
                          '@200: #50 SENT CANCELLATION TO #12: testerror\n' \
                          '@210: #12 RECEIVED CANCELLATION FROM #50: testerror\n'
        self.assertEqual(output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
