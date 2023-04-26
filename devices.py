"""This module contains the Device class that holds constant
values of each device"""

class Device:
    """This class creates a device and holds values"""
    def __init__(self):
        """Stores LENGTH, DEVICE, and PROPAGATE commands specific to its ID"""
        self.current_length = 0
        self.length = 0
        self.device_id = None
        self.propagate = []
