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
        # Run the DEVICE command
        elif command.startswith('DEVICE'):
            constants.device_number_list.append(int(command.split()[-1]))
        # Run the PROPAGATE command
        elif command.startswith('PROPAGATE'):
            device1, device2, time_pass = command.split()[1:]
            constants.propagate.append([int(device1), int(device2), int(time_pass)])
    return constants


def run_command_commands(command_list, constants):
    """Runs the 'command' commands, ALERT and CANCEL"""
    for command in command_list:
        device, message, sim_time = command.split()[1:]
        device = int(device)
        message = str(message)
        sim_time = int(sim_time)
        if command.startswith('ALERT'):
            for prop in constants.propagate:
                if int(prop[0]) == device:
                    print(f'@{sim_time}: #{device} SENT ALERT TO #{prop[1]}: {message}')
                    print(f'@{sim_time + int(prop[2])}: #{prop[1]} RECEIVED ALERT FROM #{device}: {message}')
        elif command.startswith('CANCEL'):
            for prop in constants.propagate:
                if int(prop[0]) == device:
                    print(f'@{sim_time}: #{device} SENT CANCELLATION TO #{prop[1]}: {message}')
                    print(f'@{sim_time + int(prop[2])}: #{prop[1]} RECEIVED CANCELLATION FROM #{device}: {message}')
