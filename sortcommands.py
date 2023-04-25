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


def sort_set_up_list(set_up_list) -> list:
    """Separates DEVICE and LENGTH commands from PROPAGATE"""
    devices = []
    length = None
    # Have to create new list because old is mutable
    new_set_up_list = []
    for command in set_up_list:
        # This moves DEVICE commands to different list
        if command.startswith('DEVICE'):
            devices.append(command)
        elif command.startswith('LENGTH'):
            length = int(command.split()[-1])
        else:
            new_set_up_list.append(command)
    return devices, new_set_up_list, length


def sort_command_list(command_list) -> list:
    """Sort command list so that commands will be in order of
    simulated time"""
    # The sorted function goes through the list and sorts based
    # on the value of the last integer in each command
    return sorted(command_list, key = lambda command: int(command.split()[-1]))
