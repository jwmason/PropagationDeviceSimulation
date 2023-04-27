"""This module contains the Device class that holds constant
values of each device"""


class Device:
    """This class creates a device and holds device attributes"""
    def __init__(self):
        """Stores values specific to its ID"""
        self.current_length = 0
        self.length = 0
        self.device_id = None
        self.propagate = []
        self.cancel_received = False
        self.cancel_time = 0
