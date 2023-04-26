"""This module runs the commands after filtering and sorting"""

from devices import Device


def run_device_commands(device_list, length_value) -> list:
    """Makes device objects and stores them into a list"""
    device_obj_list = []
    for device in device_list:
        device_obj = Device()
        device_obj.device_id = int(device.split()[-1])
        device_obj.length = length_value
        device_obj_list.append(device_obj)
    return device_obj_list


def run_set_up_commands(set_up_list, device_obj_list) -> list:
    """Runs the set-up commands, Storing PROPAGATE in Device"""
    for command in set_up_list:
        device1, device2, time_pass = command.split()[1:]
        # if device is first term in PROPAGATE command, add that propagation
        # to the device object
        for device in device_obj_list:
            if int(device1) == device.device_id:
                device.propagate.append([int(device1), int(device2), int(time_pass)])
    return device_obj_list


def propagate_alert(device, receiving_device, message, sim_time, device_obj_list):
    """Propagate the alert to the receiving device"""
    time_to_send = int(receiving_device[-1])
    device.current_length = sim_time + time_to_send
    if device.current_length < device.length:
        print(f'@{sim_time}: #{device.device_id} SENT ALERT TO #{receiving_device[1]}: {message}')
        print(f'@{sim_time + time_to_send}: #{receiving_device[1]} RECEIVED ALERT FROM #{device.device_id}: {message}')
        for next_receiving_device in device_obj_list:
            # Check if the next receiving device is a neighbor of the current receiving device
            if next_receiving_device.device_id == int(receiving_device[1]):
                propagate_alert(device, next_receiving_device.propagate[0], message, sim_time + time_to_send, device_obj_list)
    else:
        print(f'@{device.length}: END')


def run_command_commands(command_list, device_obj_list):
    """Runs the 'command' commands, ALERT"""
    for command in command_list:
        device, message, sim_time = command.split()[1:]
        # Set the correct types for each variable
        current_device = int(device)
        message = str(message)
        sim_time = int(sim_time)
        if command.startswith('ALERT'):
            for device in device_obj_list:
                # Checks each propagate to see if device can send ALERT
                if device.device_id == current_device:
                    for receiving_device in device.propagate:
                        propagate_alert(device, receiving_device, message, sim_time, device_obj_list)
        elif command.startswith('CANCEL'):
            for device in device_obj_list:
                # Checks each propagate to see if device can send ALERT
                if device.device_id == current_device:
                    for receiving_device in device.propagate:
                        time_to_send = int(receiving_device[-1])
                        print(f'@{sim_time}: #{device.device_id} SENT CANCELLATION TO #{receiving_device[1]}: {message}')
                        print(f'@{sim_time + time_to_send}: #{receiving_device[1]} RECEIVED CANCELLATION FROM #{device.device_id}: {message}')
