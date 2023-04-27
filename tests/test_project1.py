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
from runcommands import device_set_up, propagate_commands, alert_and_cancel_commands
from simulation import run


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
        test_devices_list, test_set_up_list, test_length_value = sort_set_up_list(test_set_up)
        expected_devices_list = ['DEVICE 50', 'DEVICE 12']
        expected_set_up_list = ['PROPAGATE 50 12 10']
        expected_length_value = 123
        self.assertEqual(test_devices_list, expected_devices_list)
        self.assertEqual(test_set_up_list, expected_set_up_list)
        self.assertEqual(test_length_value, expected_length_value)

    def test_sort_command_list(self):
        """This tests if function properly sorts the command list"""
        test_command = ['ALERT 1 ohno 100', 'CANCEL 50 testerror 3', 'CANCEL 3 test 55']
        # Testing function here
        command_list = sort_command_list(test_command)
        expected_command_list = ['CANCEL 50 testerror 3', 'CANCEL 3 test 55', 'ALERT 1 ohno 100']
        self.assertEqual(command_list, expected_command_list)


class TestRunCommands(unittest.TestCase):
    """This tests functions within runcommands.py"""
    def test_device_set_up(self):
        """Tests if device objects are created correctly"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        # Testing function here
        test_device_obj_list = device_set_up(test_device_list, 123)
        self.assertEqual(len(test_device_obj_list) ,2)
        self.assertEqual(test_device_obj_list[0].device_id, 1)
        self.assertEqual(test_device_obj_list[1].device_id, 2)
        self.assertEqual(test_device_obj_list[0].length, 123)

    def test_propagate_commands(self):
        """Tests if PROPAGATE commands are stored correctly"""
        test_set_up = ['PROPAGATE 1 2 10', 'PROPAGATE 2 1 100']
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 123)
        # Testing function here
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        self.assertEqual(test_device[0].propagate, [[1, 2, 10]])
        self.assertEqual(test_device[1].propagate, [[2, 1, 100]])

    def test_alert_and_cancel_commands(self):
        """Tests if ALERT and CANCEL commands are run correctly"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 220)
        test_set_up = ['PROPAGATE 1 2 100', 'PROPAGATE 2 1 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['ALERT 1 ohno 0', 'CANCEL 1 testerror 100']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)
        expected_output = '@0: #1 SENT ALERT TO #2: ohno\n' \
                          '@100: #2 RECEIVED ALERT FROM #1: ohno\n' \
                          '@100: #2 SENT ALERT TO #1: ohno\n' \
                          '@100: #1 SENT CANCELLATION TO #2: testerror\n' \
                          '@200: #1 RECEIVED ALERT FROM #2: ohno\n' \
                          '@200: #2 RECEIVED CANCELLATION FROM #1: testerror\n' \
                          '@220: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_alert_and_cancel_commands_edge_case_1(self):
        """Test an edge case if only one propagate command"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 150)
        test_set_up = ['PROPAGATE 1 2 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['CANCEL 1 testerror 0']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)

        expected_output = '@0: #1 SENT CANCELLATION TO #2: testerror\n' \
                          '@100: #2 RECEIVED CANCELLATION FROM #1: testerror\n' \
                          '@150: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_alert_and_cancel_commands_edge_case_2(self):
        """Test an edge case if cancellation received before alert"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 1000)
        test_set_up = ['PROPAGATE 1 2 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['CANCEL 1 testerror 0', 'ALERT 1 testerror 100', 'CANCEL 1 testerror 999']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)
        expected_output = '@0: #1 SENT CANCELLATION TO #2: testerror\n' \
                          '@100: #2 RECEIVED CANCELLATION FROM #1: testerror\n' \
                          '@1000: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_alert_and_cancel_commands_edge_case_3(self):
        """Test an edge case if device ID is equal to the receiving device"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 1000)
        test_set_up = ['PROPAGATE 1 1 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['CANCEL 1 testerror 0', 'ALERT 1 testerror 100']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)
        expected_output = '@1000: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_alert_and_cancel_commands_edge_case_4(self):
        """Also test an edge case if device ID is equal to the receiving device
        but with another cancel command afterwards"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 1000)
        test_set_up = ['PROPAGATE 1 2 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['CANCEL 1 testerror 900', 'ALERT 1 testerror 100', 'CANCEL 1 testerror 999']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)
        expected_output = '@100: #1 SENT ALERT TO #2: testerror\n' \
                            '@200: #2 RECEIVED ALERT FROM #1: testerror\n' \
                             '@1000: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_alert_and_cancel_commands_alert_edge_case_5(self):
        """Tests if command doesn't start with CANCEL or ALERT"""
        test_device_list = ['DEVICE 1', 'DEVICE 2']
        test_device_obj_list = device_set_up(test_device_list, 1000)
        test_set_up = ['PROPAGATE 1 2 100']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        # Define the command list with an ALERT command
        command_list = ['ALERT 0 Testmessage 10']
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(command_list, test_device)
        expected_output = '@1000: END\n'
        self.assertEqual(output.getvalue(), expected_output)

    def test_propagate_cancel_sample_input(self):
        """Tests sample_input and sample_output to assure success"""
        test_device_list = ['DEVICE 1', 'DEVICE 2', 'DEVICE 3', 'DEVICE 4']
        test_device_obj_list = device_set_up(test_device_list, 9999)
        test_set_up = ['PROPAGATE 1 2 750', 'PROPAGATE 2 3 1250', 'PROPAGATE 3 4 500', 'PROPAGATE 4 1 1000']
        test_device = propagate_commands(test_set_up, test_device_obj_list)
        test_command_list = ['CANCEL 1 Trouble 2200', 'ALERT 1 Trouble 0']
        # Testing function
        with contextlib.redirect_stdout(io.StringIO()) as output:
            alert_and_cancel_commands(test_command_list, test_device)
        expected_output =   '@0: #1 SENT ALERT TO #2: Trouble\n' \
                            '@750: #2 RECEIVED ALERT FROM #1: Trouble\n' \
                            '@750: #2 SENT ALERT TO #3: Trouble\n' \
                            '@2000: #3 RECEIVED ALERT FROM #2: Trouble\n' \
                            '@2000: #3 SENT ALERT TO #4: Trouble\n' \
                            '@2200: #1 SENT CANCELLATION TO #2: Trouble\n' \
                            '@2500: #4 RECEIVED ALERT FROM #3: Trouble\n' \
                            '@2500: #4 SENT ALERT TO #1: Trouble\n' \
                            '@2950: #2 RECEIVED CANCELLATION FROM #1: Trouble\n' \
                            '@2950: #2 SENT CANCELLATION TO #3: Trouble\n' \
                            '@3500: #1 RECEIVED ALERT FROM #4: Trouble\n' \
                            '@4200: #3 RECEIVED CANCELLATION FROM #2: Trouble\n' \
                            '@4200: #3 SENT CANCELLATION TO #4: Trouble\n' \
                            '@4700: #4 RECEIVED CANCELLATION FROM #3: Trouble\n' \
                            '@4700: #4 SENT CANCELLATION TO #1: Trouble\n' \
                            '@5700: #1 RECEIVED CANCELLATION FROM #4: Trouble\n' \
                            '@9999: END\n'
        self.assertEqual(output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
