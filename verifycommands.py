def get_commands(input_list) -> list:
    """Stores and returns all possible commands into a list"""
    cmd_list = []
    for cmd in input_list:
        # Splits the command by space and grabs the first word to see if it is a command or not
        first_word = cmd.split()[0]
        all_possible_cmds = ['LENGTH', 'DEVICE', 'PROPAGATE', 'ALERT', 'CANCEL']
        # If line is a possible command, adds to command list
        if first_word in all_possible_cmds:
            cmd_list.append(cmd)
        else:
            pass
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
            if len(command_word_length) == 2:
                pass
            else:
                cmd_list.remove(cmd)
        # Checking that PROPAGATE, ALERT, and CANCEL commands have three parameters
        elif first_word == 'PROPAGATE' or first_word == 'ALERT' or first_word == 'CANCEL':
            if len(command_word_length) == 3:
                pass
            else:
                cmd_list.remove(cmd)
    return cmd_list

        # supposed_positive_integer_value = command_word_length[1]
        # if type(supposed_positive_integer_value) is int and supposed_positive_integer_value > 0:
        #     pass
        # else:
        #     cmd_list.remove(cmd)