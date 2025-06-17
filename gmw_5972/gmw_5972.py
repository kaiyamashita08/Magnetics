import time
import nidaqmx
from nidaqmx.constants import LineGrouping, TerminalConfiguration

class GMW5972:
    """
    Based on the ports specified in the GMW 5972 User's Manual,
    https://gmw.com/wp-content/uploads/2023/04/UM5972-XT_Rev-A_May_2024.pdf?srsltid=AfmBOooe7Xox6S9XkC7NIE0X3ask7ZvgjSdxgHFiBm9J_Q-oxgi9R0Gv
    on page 31
    Covers all functionality for the old version of the GMW 5972, but not the newer one.
    """

    def __init__(self, dev="Dev2",
                 max_current = 70.0,
                 max_voltage = 85.0,
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
        self.dev = dev
        self.max_current = max_current
        self.max_voltage = max_voltage
        self.field_gain = field_sensor_V_per_T
        self.current_per_T = current_per_T

        # Analog Outputs
        self.ao = type("AOChannels", (), {})()

        # Current Control (AO-0)
        self.ao.current_task = nidaqmx.Task()
        self.ao.current_chan = f"{dev}/ao0"
        self.ao.current_task.ao_channels.add_ao_voltage_chan(
            self.ao.current_chan,
            min_val=-10.0, max_val=10.0
        )

        # Analog Inputs
        self.ai = type("AIChannels", (), {})()

        # Voltage Monitor (AI-0)
        self.ai.voltage_task = nidaqmx.Task()
        self.ai.voltage_chan = f"{dev}/ai0"
        self.ai.voltage_task.ai_channels.add_ai_voltage_chan(
            self.ai.voltage_chan,
            terminal_config=TerminalConfiguration.RSE,
            min_val=-10, max_val=10
        )

        # Current Monitor (AI-1)
        self.ai.current_task = nidaqmx.Task()
        self.ai.current_chan = f"{dev}/ai1"
        self.ai.current_task.ai_channels.add_ai_voltage_chan(
            self.ai.current_chan,
            terminal_config=TerminalConfiguration.RSE,
            min_val=-10, max_val=10
        )

        # Field Monitor (AI-2/AI-10, differential)
        self.ai.field_task = nidaqmx.Task()
        self.ai.field_chan = f"{dev}/ai2"
        self.ai.field_task.ai_channels.add_ai_voltage_chan(
            self.ai.field_chan,
            terminal_config=TerminalConfiguration.DIFF,
            min_val=-10, max_val=10
        )

        # Digital inputs/outputs
        self.di = type("DIChannels", (), {})()

        # Flow Interlock
        self.di.flow_interlock_task = nidaqmx.Task()
        self.di.flow_interlock_chan = f"{dev}/port0/line2"
        self.di.flow_interlock_task.di_channels.add_di_chan(
            self.di.flow_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        # Temperature Interlock
        self.di.temp_interlock_task = nidaqmx.Task()
        self.di.temp_interlock_chan = f"{dev}/port0/line3"
        self.di.temp_interlock_task.di_channels.add_di_chan(
            self.di.temp_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        # General Interlock
        self.di.general_interlock_task = nidaqmx.Task()
        self.di.general_interlock_chan = f"{dev}/port1/line0"
        self.di.general_interlock_task.di_channels.add_di_chan(
            self.di.general_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        # EPO Trip Interlock
        self.di.epo_trip_interlock_task = nidaqmx.Task()
        self.di.epo_trip_interlock_chan = f"{dev}/port1/line1"
        self.di.epo_trip_interlock_task.di_channels.add_di_chan(
            self.di.epo_trip_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        # Power Supply Status
        self.di.ps_enabled_task = nidaqmx.Task()
        self.di.ps_enabled_chan = f"{dev}/port0/line4"
        self.di.ps_enabled_task.di_channels.add_di_chan(
            self.di.ps_enabled_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        # Digital Outputs
        self.do = type("DOChannels", (), {})()

        # Local Lockout Control
        self.do.lockout_task = nidaqmx.Task()
        self.do.lockout_chan = f"{dev}/port0/line6"
        self.do.lockout_task.do_channels.add_do_chan(
            self.do.lockout_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

    def set_lockout(self, state):
        """
        Set the lockout of the Magnet Control.
        This should always be turned on whenever the magnet is controlled, and turned off afterward.
        :param state: The state of the lockout (True = Local Lockout)
        """
        self.do.lockout_task.write(bool(state))

    def set_current(self, amps):
        """
        Set the current of the power supply to the magnet
        :param amps: The current in amps
        """
        voltage = amps * 10 / self.max_current
        self.ao.current_task.write(voltage)

    def get_current(self):
        """
        Get the current of the power supply in amps
        :return: The current of the power supply in amps
        """
        voltage = self.ai.current_task.read()
        return voltage / 10 * self.max_current

    def get_voltage(self):
        """
        Get the voltage of the power supply in amps
        :return: The voltage of the power supply in amps
        """
        voltage = self.ai.voltage_task.read()
        return voltage / 10 * self.max_voltage

    def get_field(self):
        """
        Get the magnetic field from a connected sensor
        :return: The magnetic field in Teslas
        """
        voltage = self.ai.field_task.read()
        return voltage / self.field_gain

    def magnet_flow_interlock(self):
        """
        Get the status of the magnet flow interlock
        :return: The status, where True = good
        """
        return not bool(self.di.flow_interlock_task.read())

    def temperature_interlock(self):
        """
        Get the status of the temperature interlock
        :return: The status, where True = good
        """
        return not bool(self.di.temp_interlock_task.read())

    def general_interlock(self):
        """
        Get the status of the general interlock
        :return: The status, where True = good
        """
        return not bool(self.di.general_interlock_task.read())

    def epo_trip_interlock(self):
        """
        Get the status of the EPO trip interlock
        :return: The status, where True = good
        """
        return not bool(self.di.epo_trip_interlock_task.read())

    def power_supply_enabled(self):
        """
        Get whether the power supply is enabled
        :return: True if the power supply is enabled, False otherwise
        """
        return bool(self.di.ps_enabled_task.read())

    def close(self):
        """
        Close the tasks - must be run at the end of every program
        """
        self.ao.current_task.close()

        self.ai.field_task.close()
        self.ai.current_task.close()
        self.ai.voltage_task.close()

        self.di.flow_interlock_task.close()
        self.di.temp_interlock_task.close()
        self.di.general_interlock_task.close()
        self.di.epo_trip_interlock_task.close()

        self.di.ps_enabled_task.close()

        self.do.lockout_task.close()