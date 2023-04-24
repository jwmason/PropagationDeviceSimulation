"""This module runs the commands after filtering and sorting"""

from commandconstants import Constants


def run_set_up_commands(set_up_list) -> Constants:
    """Runs the set-up commands, LENGTH and DEVICE, then PROPAGATE"""
    # Initialize a Constants class
    constants = Constants()
    for command in set_up_list:
        # Run the LENGTH command
        if command.startswith('LENGTH'):
            constants.length = int(command.split()[-1])
        elif command.startswith('DEVICE'):
            constants.device_number_list.append(int(command.split()[-1]))
        elif command.startswith('PROPAGATE'):
            device1, device2, time_pass = command.split()[1:]
            constants.propagate.append([int(device1), int(device2), int(time_pass)])
    return constants
