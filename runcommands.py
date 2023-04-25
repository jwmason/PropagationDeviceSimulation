"""This module runs the commands after filtering and sorting"""

from devices import Device


def run_device_commands(device_list, length_value) -> list:
    """Makes device objects and stores them into a list"""
    device_obj_list = []
    for device in device_list:
        device_obj = Device()
        device_obj.device_id = int(device[-1])
        device_obj.length = length_value
        device_obj_list.append(device_obj)
    return device_obj_list


def run_set_up_commands(set_up_list, device_obj_list) -> list:
    """Runs the set-up commands, Storing PROPAGATE in Device"""
    for command in set_up_list:
        device1, device2, time_pass = command.split()[1:]
        for device in device_obj_list:
            if int(device1) == device.device_id:
                device.propagate.append([int(device2), int(time_pass)])
    return device_obj_list


def run_command_commands(command_list, device_obj_list):
    """Runs the 'command' commands, ALERT and CANCEL"""
    for command in command_list:
        device, message, sim_time = command.split()[1:]
        # Set the correct types for each variable
        device = int(device)
        message = str(message)
        sim_time = int(sim_time)
        if command.startswith('ALERT'):
            for device in device_obj_list:
                # Checks each propagate to see if device can send ALERT
                if device.device_id == device:
                    for receiving_device in device.propagate:
                        print(f'@{sim_time}: #{device} SENT ALERT TO #{receiving_device[0]}: {message}')
                    print(f'@{sim_time + int(prop[2])}: #{prop[1]} RECEIVED ALERT FROM #{device}: {message}')
                    for prop2 in constants.propagate:
                        if int(prop[1]) == prop2[0]:
                            print(f'@{sim_time}: #{prop[1]} SENT ALERT TO #{prop2[1]}: {message}')
                            print(f'@{sim_time + int(prop2[2])}: #{prop2[1]} RECEIVED ALERT FROM #{prop[1]}: {message}')
        elif command.startswith('CANCEL'):
            for prop in constants.propagate:
                # Checks each propagate to see if device can send CANCEL
                if int(prop[0]) == device:
                    print(f'@{sim_time}: #{device} SENT CANCELLATION TO #{prop[1]}: {message}')
                    print(f'@{sim_time + int(prop[2])}: #{prop[1]} RECEIVED CANCELLATION FROM #{device}: {message}')
                    for prop2 in constants.propagate:
                        if int(prop[1]) == prop2[0]:
                            print(f'@{sim_time}: #{prop[1]} SENT CANCELLATION TO #{prop2[1]}: {message}')
                            print(
                                f'@{sim_time + int(prop2[2])}: #{prop2[1]} RECEIVED CANCELLATION FROM #{prop[1]}: {message}')