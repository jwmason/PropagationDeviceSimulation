"""This module is in charge of sorting the commands so that
they run in the correct order"""

def sort_cmd_list(cmd_list) -> list:
    """This function will sort the set-up commands from the
    'command' commands"""
    # This list will contain the commands I want to run first
    set_up_list = []
    # This list will contain the commands I want to run after the
    # set-up commands are initialized
    command_list = []
    for command in cmd_list:
        # Separating LENGTH, DEVICE, and PROPAGATE commands as set-up commands
        if command.startswith('LENGTH') or command.startswith('DEVICE') or command.startswith('PROPAGATE'):
            set_up_list.append(command)
        else:
            command_list.append(command)
    return set_up_list, command_list

