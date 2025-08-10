import random

class GMW5972:
    """
    Simulated class for the GMW5972 controller, to be used when testing software when disconnected
    """

    current_per_T = 21.8
    current = 0

    def __init__(self, dev="Dev2",
                 max_current=70.0,
                 max_voltage=85.0,
                 field_sensor_V_per_T=5.0,
                 current_per_T=21.8):
        # TODO: Figure out whether current_per_T is needed
        """
        Initialize a GMW5972 Controller
        :param dev: The identity of the controller
        :param max_current: The max current of the power supply
        :param max_voltage: The max voltage of the power supply
        :param field_sensor_V_per_T: The voltage per Tesla that the field sensor outputs
        :param current_per_T: Potentially useless
        """

    def set_lockout(self, state):
        """
        Set the lockout of the Magnet Control.
        This should always be turned on whenever the magnet is controlled, and turned off afterward.
        :param state: The state of the lockout (True = Local Lockout)
        """
        print(f"Setting lockout: {state}")

    def set_current(self, amps):
        """
        Set the current of the power supply to the magnet
        :param amps: The current in amps
        """
        self.current = amps
        print(f"Setting current: {amps} amps")

    def get_current(self):
        """
        Get the current of the power supply in amps
        :return: The current of the power supply in amps
        """
        return self.current + 2 * random.random() - 1

    def get_voltage(self):
        """
        Get the voltage of the power supply in amps
        :return: The voltage of the power supply in amps
        """
        return self.current * 0.7 + 0.8 * random.random() - 0.4

    def get_field(self):
        """
        Get the magnetic field from a connected sensor
        :return: The magnetic field in Teslas
        """
        return self.current / self.current_per_T + 0.1 * random.random() - 0.05

    def magnet_flow_interlock(self):
        """
        Get the status of the magnet flow interlock
        :return: The status, where True = good
        """
        return True

    def temperature_interlock(self):
        """
        Get the status of the temperature interlock
        :return: The status, where True = good
        """
        return True

    def general_interlock(self):
        """
        Get the status of the general interlock
        :return: The status, where True = good
        """
        return True

    def epo_trip_interlock(self):
        """
        Get the status of the EPO trip interlock
        :return: The status, where True = good
        """
        return True

    def power_supply_enabled(self):
        """
        Get whether the power supply is enabled
        :return: True if the power supply is enabled, False otherwise
        """
        return True

    def close(self):
        """
        Close the tasks - must be run at the end of every program
        """