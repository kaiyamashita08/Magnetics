import time
import nidaqmx
from nidaqmx.constants import LineGrouping, TerminalConfiguration

class GMW5972:
    def __init__(self, dev="Dev2",
                 digital_output_line="port0/line6",
                 max_current = 70.0,
                 max_voltage = 85.0,
                 field_sensor_V_per_T=5.0,
                 current_per_T=21.8):
        """
        Initialize the magnet controller interface based on GMW 5972 + NI USB-6251 connections.
        """

        self.dev = dev
        self.max_current = max_current
        self.max_voltage = max_voltage
        self.field_gain = field_sensor_V_per_T
        self.current_per_T = current_per_T

        # Analog output: current control (AO-0)
        self.ao = type("AOChannels", (), {})()
        self.ao.current_task = nidaqmx.Task()
        self.ao.current_chan = f"{dev}/ao0"
        self.ao.current_task.ao_channels.add_ao_voltage_chan(
            self.ao.current_chan,
            min_val=-10.0, max_val=10.0
        )

        # Analog input: current monitor (AI-1)
        self.ai = type("AIChannels", (), {})()
        self.ai.current_task = nidaqmx.Task()
        self.ai.current_chan = f"{dev}/ai1"
        self.ai.current_task.ai_channels.add_ai_voltage_chan(
            self.ai.current_chan,
            terminal_config=TerminalConfiguration.RSE,
            min_val=-10, max_val=10
        )

        self.ai.voltage_task = nidaqmx.Task()
        self.ai.voltage_chan = f"{dev}/ai0"
        self.ai.voltage_task.ai_channels.add_ai_voltage_chan(
            self.ai.voltage_chan,
            terminal_config=TerminalConfiguration.RSE,
            min_val=-10, max_val=10
        )

        # Analog input: field monitor (AI-2/AI-10, differential)
        self.ai.field_task = nidaqmx.Task()
        self.ai.field_chan = f"{dev}/ai2"
        self.ai.field_task.ai_channels.add_ai_voltage_chan(
            self.ai.field_chan,
            terminal_config=TerminalConfiguration.DIFF,
            min_val=-10, max_val=10
        )

        # Digital inputs/outputs
        self.di = type("DIChannels", (), {})()

        # Interlocks
        self.di.flow_interlock_task = nidaqmx.Task()
        self.di.flow_interlock_chan = f"{dev}/port0/line2"
        self.di.flow_interlock_task.di_channels.add_di_chan(
            self.di.flow_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.di.temp_interlock_task = nidaqmx.Task()
        self.di.temp_interlock_chan = f"{dev}/port0/line3"
        self.di.temp_interlock_task.di_channels.add_di_chan(
            self.di.temp_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.di.general_interlock_task = nidaqmx.Task()
        self.di.general_interlock_chan = f"{dev}/port1/line0"
        self.di.general_interlock_task.di_channels.add_di_chan(
            self.di.general_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.di.epo_trip_interlock_task = nidaqmx.Task()
        self.di.epo_trip_interlock_chan = f"{dev}/port1/line1"
        self.di.epo_trip_interlock_task.di_channels.add_di_chan(
            self.di.epo_trip_interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)


        self.di.ps_enabled_task = nidaqmx.Task()
        self.di.ps_enabled_chan = f"{dev}/port0/line4"
        self.di.ps_enabled_task.di_channels.add_di_chan(
            self.di.ps_enabled_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.do = type("DOChannels", (), {})()
        self.do.lockout_task = nidaqmx.Task()
        self.do.lockout_chan = f"{dev}/port0/line6"
        self.do.lockout_task.do_channels.add_do_chan(
            self.do.lockout_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

    def set_lockout(self, state):
        self.do.lockout_task.write(bool(state))

    def set_current(self, amps):
        voltage = amps * 10 / self.max_current
        self.ao.current_task.write(voltage)

    def get_current(self):
        voltage = self.ai.current_task.read()
        return voltage / 10 * self.max_current

    def get_voltage(self):
        voltage = self.ai.voltage_task.read()
        return voltage / 10 * self.max_voltage

    def get_field(self):
        voltage = self.ai.field_task.read()
        return voltage / self.field_gain

    def magnet_flow_interlock(self):
        return not bool(self.di.flow_interlock_task.read())

    def temperature_interlock(self):
        return not bool(self.di.temp_interlock_task.read())

    def general_interlock(self):
        return not bool(self.di.general_interlock_task.read())

    def epo_trip_interlock(self):
        return not bool(self.di.epo_trip_interlock_task.read())

    def power_supply_enabled(self):
        return bool(self.di.ps_enabled_task.read())

    def close(self):
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