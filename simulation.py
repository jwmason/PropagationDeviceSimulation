"""This module groups all sub modules and runs the program in entirety"""

from readinput import _read_input_file_path, read_input_file_contents
from verifycommands import get_commands, verify_commands_length, verify_commands_parameters
from sortcommands import sort_cmd_list, sort_set_up_list, sort_command_list
from runcommands import run_set_up_commands, run_command_commands

def run() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    read_contents = read_input_file_contents(input_file_path)
    cmd_list1 = get_commands(read_contents)
    print(cmd_list1)
    cmd_list2 = verify_commands_length(cmd_list1)
    cmd_list3 = verify_commands_parameters(cmd_list2)
    set_up_list, command_list = sort_cmd_list(cmd_list3)
    set_up_list = sort_set_up_list(set_up_list)
    command_list = sort_command_list(command_list)
    constants = run_set_up_commands(set_up_list)
    run_command_commands(command_list, constants)
