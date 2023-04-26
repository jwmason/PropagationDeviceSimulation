"""This module runs the commands after filtering and sorting"""

from devices import Device
from sortoutput import Output

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


def propagate_alert(device, receiving_device, message, sim_time, device_obj_list, output_storage):
    """Propagate the alert to the receiving device"""
    time_to_send = int(receiving_device[-1])
    # Setting current simulated time
    device.current_length = sim_time
    # Only execute if within simulated time length
    if (device.current_length + time_to_send) < device.length:
        if device.device_id != int(receiving_device[1]):
            if (device.cancel_received is True and device.current_length < device.cancel_time) or (device.cancel_received is False and device.current_length < device.length):
                output_storage.output.append(f'@{sim_time}: #{device.device_id} SENT ALERT TO #{receiving_device[1]}: {message}')
                output_storage.output.append(f'@{sim_time + time_to_send}: #{receiving_device[1]} RECEIVED ALERT FROM #{device.device_id}: {message}')
                for next_receiving_device in device_obj_list:
                    # Check if the next receiving device is a neighbor of the current receiving device
                    if next_receiving_device.device_id == int(receiving_device[1]):
                        return propagate_alert(next_receiving_device, next_receiving_device.propagate[0], message, sim_time + time_to_send, device_obj_list, output_storage)
        else:
            return True
    else:
        return False


def propagate_cancel(device, receiving_device, message, sim_time, device_obj_list, output_storage):
    """Propagate the cancel to the receiving device"""
    time_to_send = int(receiving_device[-1])
    # Setting current simulated time
    device.current_length = sim_time
    # Only execute if within simulated time length
    if (device.current_length + time_to_send) < device.length:
        if device.device_id != int(receiving_device[1]):
            output_storage.output.append(f'@{sim_time}: #{device.device_id} SENT CANCELLATION TO #{receiving_device[1]}: {message}')
            output_storage.output.append(f'@{sim_time + time_to_send}: #{receiving_device[1]} RECEIVED CANCELLATION FROM #{device.device_id}: {message}')
            device.cancel_received = True
            device.cancel_time = sim_time
            for next_receiving_device in device_obj_list:
                # Check if the next receiving device is a neighbor of the current receiving device
                if next_receiving_device.device_id == int(receiving_device[1]) and next_receiving_device.cancel_received is False:
                    next_receiving_device.cancel_received = True
                    next_receiving_device.cancel_time = sim_time
                    return propagate_cancel(next_receiving_device, next_receiving_device.propagate[0], message, sim_time + time_to_send, device_obj_list, output_storage)
        else:
            output_storage.output.append(f'@{sim_time + time_to_send}: #{receiving_device[1]} RECEIVED CANCELLATION FROM #{receiving_device[0]}: {message}')
            return True
    else:
        return False


def run_command_commands(command_list, device_obj_list):
    """Runs the 'command' commands, ALERT"""
    output_storage = Output()
    for command in command_list:
        device, message, sim_time = command.split()[1:]
        # Set the correct types for each variable
        current_device = int(device)
        message = str(message)
        sim_time = int(sim_time)
        if command.startswith('CANCEL'):
            cancel_propagated = False
            for device in device_obj_list:
                # Checks each propagate to see if device can send ALERT
                if device.device_id == current_device:
                    for receiving_device in device.propagate:
                        if propagate_cancel(device, receiving_device, message, sim_time,
                                           device_obj_list, output_storage):
                            cancel_propagated = True
            # This is raised when the simulated time is greater than simulated length
            if cancel_propagated:
                output_storage.output.append(f'@{device.length}: END')
        elif command.startswith('ALERT'):
            alert_propagated = False
            for device in device_obj_list:
                # Checks each propagate to see if device can send ALERT
                if device.device_id == current_device:
                    for receiving_device in device.propagate:
                        if propagate_alert(device, receiving_device, message, sim_time,
                                           device_obj_list, output_storage):
                            alert_propagated = True
            # This is raised when the simulated time is greater than simulated length
            if alert_propagated:
                pass
    output_storage.output.append(f'@{device.length}: END')
    for output in sorted(output_storage.output, key=lambda x: int(x.split('@')[-1].split(':')[0]) if '@' in x else -1):
        print(output)
