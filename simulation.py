"""This module groups all sub-modules and runs the program in entirety"""

# Importing all sub-modules here
from readinput import _read_input_file_path, read_input_file_contents
from verifycommands import get_commands, verify_commands_length, verify_commands_parameters
from sortcommands import sort_cmd_list, sort_set_up_list, sort_command_list
from runcommands import device_set_up, propagate_commands, alert_and_cancel_commands

# Function Not Test Covered:
# No test coverage for this module because it simply runs all the sub-modules that
# are already being tested, so testing this will not provide anymore coverage.
# Also since readinput.py functions require input, this cannot be tested
def run() -> None:
    """Runs all sub-modules in program entirety"""
    # readinput.py
    input_file_path = _read_input_file_path()
    read_contents = read_input_file_contents(input_file_path)
    # verifycommands.py
    cmd_list1 = get_commands(read_contents)
    cmd_list2 = verify_commands_length(cmd_list1)
    cmd_list3 = verify_commands_parameters(cmd_list2)
    # sortcommands.py
    set_up_list, command_list = sort_cmd_list(cmd_list3)
    devices, set_up_list, length = sort_set_up_list(set_up_list)
    command_list = sort_command_list(command_list)
    # runcommands.py
    test_device_obj_list = device_set_up(devices, length)
    device_obj_list = propagate_commands(set_up_list, test_device_obj_list)
    alert_and_cancel_commands(command_list, device_obj_list)
