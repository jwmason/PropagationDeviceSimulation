def get_commands(input_list) -> list:
    """Stores and returns all possible commands into a list"""
    cmd_list = []
    for cmd in input_list:
        # Splits the command by space and grabs the first word
        # to see if it is a command or not
        first_word = cmd.split()[0]
        all_possible_cmds = ['LENGTH', 'DEVICE', 'PROPAGATE', 'ALERT', 'CANCEL']
        # If line is a possible command, adds to command list
        if first_word in all_possible_cmds:
            cmd_list.append(cmd)
        else:
            pass
    return cmd_list
