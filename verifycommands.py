"""This module is in charge of verifying commands from input file"""
def get_commands(input_list) -> list:
    """Stores and returns all possible commands into a list"""
    cmd_list = []
    for cmd in input_list:

        print(input_list)
        # Splits the command by space and grabs the first word to see if it is a command or not
        if (cmd != '\n') and (cmd != ' \n'):
            first_word = cmd.split()[0]
        all_possible_cmds = ['LENGTH', 'DEVICE', 'PROPAGATE', 'ALERT', 'CANCEL']
        # If line is a possible command, adds to command list
        if first_word in all_possible_cmds:
            cmd = cmd.strip('\n')
            cmd_list.append(cmd)
    return cmd_list


def verify_commands_length(cmd_list) -> list:
    """Checks each command to see if it has the correct
     amount of parameters following the possible command word"""
    for cmd in cmd_list:
        command_word_length = cmd.split()
        # See what command is being called so I can verify how many parameters are needed
        first_word = command_word_length[0]
        # Checking that LENGTH and DEVICE commands have one parameter
        if first_word == 'LENGTH' or first_word == 'DEVICE':
            if not len(command_word_length) == 2:
                cmd_list.remove(cmd)
        # Checking that PROPAGATE, ALERT, and CANCEL commands have three parameters
        elif first_word == 'PROPAGATE' or first_word == 'ALERT' or first_word == 'CANCEL':
            if not len(command_word_length) == 4:
                cmd_list.remove(cmd)
    return cmd_list


def verify_commands_parameters(cmd_list) -> list:
    """Check if the parameters in each command are valid"""
    length_dict = {}
    valid_cmds = []
    for cmd in cmd_list:
        command_word_length = cmd.split()
        length_word = next((word for word in command_word_length if word.startswith('LENGTH')), None)
        if length_word is not None:
            length_value = int(command_word_length[command_word_length.index(length_word) + 1])
            length_dict[length_word] = length_value

        # See what command is being called so I can verify how many parameters are being verified
        first_word = command_word_length[0]
        # Checking that LENGTH and DEVICE commands have one positive integer value
        if first_word == 'LENGTH' or first_word == 'DEVICE':
            supposed_positive_integer_value = command_word_length[1]
            if not type(supposed_positive_integer_value) is int and int(supposed_positive_integer_value) > 0:
                valid_cmds.append(cmd)
        # Checking that PROPAGATE three positive integer values, and that those devices exist
        elif first_word == 'PROPAGATE':
            device_1, device_2, time_pass = command_word_length[1:]
            device_1 = int(device_1)
            device_2 = int(device_2)
            if (type(device_1) is int and device_1 > 0) and (type(device_2) is int and device_2 > 0):
                device_1 = 'DEVICE ' + str(device_1)
                device_2 = 'DEVICE ' + str(device_2)
                print(device_1, device_2)
                if (device_1 in cmd_list) and (device_2 in cmd_list):
                    valid_cmds.append(cmd)
            else:
                valid_cmds.append(cmd)
            if not type(time_pass) is int and int(time_pass) > 0:
                continue
            else:
                valid_cmds.append(cmd)
        # Checking that ALERT and CANCEL have positive integer, string,
        # and then another positive integer
        elif first_word == 'ALERT' or first_word == 'CANCEL':
            device, message, time = command_word_length[1:]
            if type(device) is int and device > 0:
                device = 'DEVICE ' + str(device)
                if device not in cmd_list:
                    valid_cmds.append(cmd)
            else:
                valid_cmds.append(cmd)
            if not (type(time) is int and int(time) > 0) and (int(time) < int(length_dict['LENGTH'])):
                continue
            else:
                valid_cmds.append(cmd)
    return valid_cmds
