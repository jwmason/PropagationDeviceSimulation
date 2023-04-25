"""This module is in charge of verifying commands from input file"""

from length import Length


def get_commands(input_list) -> list:
    """Stores and returns all possible commands into a list"""
    cmd_list = []
    for cmd in input_list:
        # Splits the command by space and grabs the first word to see if it is a command or not
        if (cmd != '\n') and (cmd != ' \n') and (cmd != ''):
            first_word = cmd.split()[0]
        all_possible_cmds = ['LENGTH', 'DEVICE', 'PROPAGATE', 'ALERT', 'CANCEL']
        # If line is a possible command, adds to command list
        if first_word in all_possible_cmds and first_word is not None:
            # Get rid of the '\n' at the end of each line
            cmd = cmd.strip('\n')
            cmd_list.append(cmd)
    # Remove empty strings from the list
    cmd_list = list(filter(None, cmd_list))
    return cmd_list


def verify_commands_length(cmd_list) -> list:
    """Checks each command to see if it has the correct
     amount of parameters following the possible command word"""
    valid_cmds = []
    for cmd in cmd_list:
        command_word_length = cmd.split()
        # See what command is being called so I can verify how many parameters are needed
        first_word = command_word_length[0]
        # Checking that LENGTH and DEVICE commands have one parameter
        if first_word == 'LENGTH' or first_word == 'DEVICE':
            if len(command_word_length) == 2:
                valid_cmds.append(cmd)
        # Checking that PROPAGATE, ALERT, and CANCEL commands have three parameters
        if first_word == 'PROPAGATE' or first_word == 'ALERT' or first_word == 'CANCEL':
            if len(command_word_length) == 4:
                valid_cmds.append(cmd)
    return valid_cmds


def verify_commands_parameters(cmd_list) -> list:
    """Check if the parameters in each command are valid"""
    length_dict = {}
    valid_cmds = []

    for cmd in cmd_list:

        # Split each command by whitespace
        command_word_length = cmd.split()
        length_dict = get_length(command_word_length, length_dict)

        # See what command is being called so I can verify how many parameters are being verified
        first_word = command_word_length[0]

        # Adding valid length and device commands to command list
        check_length_and_device(command_word_length, first_word, cmd, valid_cmds)

        # Adding valid propagate commands to command list
        check_propagate(command_word_length, first_word, cmd, valid_cmds, cmd_list)

        # Adding valid alert and cancel commands to command list
        check_alert_and_cancel(command_word_length, first_word, cmd, valid_cmds, cmd_list, length_dict)

    return valid_cmds


def get_length(command_word_length, length_dict) -> dict:
    """Gets the length value of the command list to use for later use"""
    length_word = next((word for word in command_word_length if word.startswith('LENGTH')), None)
    if length_word is not None:
        length_value = int(command_word_length[command_word_length.index(length_word) + 1])
        length_dict[length_word] = length_value
        length_class = Length()
        length_class.length = length_value
    return length_dict


def check_length_and_device(command_word_length, first_word, cmd, valid_cmds) -> None:
    """Checking that LENGTH and DEVICE commands have one positive integer value"""
    if first_word == 'LENGTH' or first_word == 'DEVICE':
        supposed_positive_integer_value = command_word_length[1]
        try:
            if int(supposed_positive_integer_value) > 0:
                valid_cmds.append(cmd)
        except ValueError:
            pass

def check_propagate(command_word_length, first_word, cmd, valid_cmds, cmd_list) -> None:
    """Checking that PROPAGATE three positive integer values, and that those devices exist"""
    if first_word == 'PROPAGATE':
        device_1, device_2, time_pass = command_word_length[1:]
        try:
            device_1 = int(device_1)
            device_2 = int(device_2)
            time_pass = int(time_pass)
            if device_1 > 0 and device_2 > 0 and time_pass > 0:
                device_1 = 'DEVICE ' + str(device_1)
                device_2 = 'DEVICE ' + str(device_2)
                if (device_1 in cmd_list) and (device_2 in cmd_list):
                    valid_cmds.append(cmd)
        except ValueError:
            pass


def check_alert_and_cancel(command_word_length, first_word, cmd, valid_cmds, cmd_list, length_dict) -> None:
    """Checking that ALERT and CANCEL have positive integer, string,
    and then another positive integer"""
    if first_word == 'ALERT' or first_word == 'CANCEL':
        device, message, time = command_word_length[1:]
        try:
            device = int(device)
            message = str(message)
            time = int(time)
            if device > 0 and time >= 0 and (time < int(length_dict['LENGTH'])):
                device = 'DEVICE ' + str(device)
                if device in cmd_list:
                    valid_cmds.append(cmd)
        except ValueError:
            pass
