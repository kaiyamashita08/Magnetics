import time
import nidaqmx
from nidaqmx.constants import LineGrouping, TerminalConfiguration

class GMW5972:
    """
    Python driver class for controlling a GMW 5972 magnet controller using NI-DAQmx interface.
    """
    def __init__(self, dev="Dev1",
                 ao_channel="ao0",
                 ai_current="ai1",
                 ai_field_pos="ai2",
                 ai_field_neg="ai10",
                 interlock_digital_line="port0/line2",
                 digital_output_line="port0/line6",
                 temp_ok_line="port0/line3",
                 ps_enabled_line="port0/line4",
                 gain_V_per_A=0.735,
                 field_sensor_V_per_T=5.0,
                 current_per_T=21.8):
        """
        Initialize the magnet controller interface based on GMW 5972 + NI USB-6251 connections.
        """
        self.dev = dev
        self.gain = gain_V_per_A
        self.field_gain = field_sensor_V_per_T
        self.current_per_T = current_per_T

        # Analog output: current control (AO-0)
        self.ao = type("AOChannels", (), {})()
        self.ao.current_task = nidaqmx.Task()
        self.ao.current_chan = f"{dev}/{ao_channel}"
        self.ao.current_task.ao_channels.add_ao_voltage_chan(self.ao.current_chan, min_val=-10.0, max_val=10.0)

        # Analog input: current monitor (AI-1)
        self.ai = type("AIChannels", (), {})()
        self.ai.current_task = nidaqmx.Task()
        self.ai.current_chan = f"{dev}/{ai_current}"
        self.ai.current_task.ai_channels.add_ai_voltage_chan(self.ai.current_chan, min_val=-10.0, max_val=10.0)

        # Analog input: field monitor (AI-2/AI-10, differential)
        self.ai.field_task = nidaqmx.Task()
        self.ai.field_chan = f"{dev}/{ai_field_pos}"
        self.ai.field_task.ai_channels.add_ai_voltage_chan(
            self.ai.field_chan,
            terminal_config=TerminalConfiguration.DIFF,
            min_val=-10.0, max_val=10.0
        )

        # Digital inputs/outputs
        self.di = type("DIChannels", (), {})()

        self.di.interlock_task = nidaqmx.Task()
        self.di.interlock_chan = f"{dev}/{interlock_digital_line}"
        self.di.interlock_task.di_channels.add_di_chan(
            self.di.interlock_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.di.temp_ok_task = nidaqmx.Task()
        self.di.temp_ok_chan = f"{dev}/{temp_ok_line}"
        self.di.temp_ok_task.di_channels.add_di_chan(
            self.di.temp_ok_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.di.ps_enabled_task = nidaqmx.Task()
        self.di.ps_enabled_chan = f"{dev}/{ps_enabled_line}"
        self.di.ps_enabled_task.di_channels.add_di_chan(
            self.di.ps_enabled_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.do = type("DOChannels", (), {})()
        self.do.control_task = nidaqmx.Task()
        self.do.control_chan = f"{dev}/{digital_output_line}"
        self.do.control_task.do_channels.add_do_chan(
            self.do.control_chan, line_grouping=LineGrouping.CHAN_PER_LINE)

    def set_current(self, amps):
        voltage = amps * self.gain
        self.ao.current_task.write(voltage)

    def set_field(self, field_T):
        if self.current_per_T is None:
            raise RuntimeError("Magnet calibration (A/T) not defined.")
        target_current = field_T * self.current_per_T
        self.set_current(target_current)

    def get_current(self):
        voltage = self.ai.current_task.read()
        return voltage / self.gain

    def get_field(self):
        voltage = self.ai.field_task.read()
        return voltage / self.field_gain

    def interlock_ok(self):
        return bool(self.di.interlock_task.read())

    def temperature_ok(self):
        return bool(self.di.temp_ok_task.read())

    def power_supply_enabled(self):
        return bool(self.di.ps_enabled_task.read())

    def set_digital_output(self, state):
        self.do.control_task.write(bool(state))

    def ramp_current(self, target_amps, rate_amps_per_s=0.1, dt=0.05):
        current = self.get_current()
        steps = max(int(abs(target_amps - current) / (rate_amps_per_s * dt)), 1)
        for i in range(1, steps + 1):
            intermediate = current + (target_amps - current) * i / steps
            if not self.interlock_ok():
                raise RuntimeError("Interlock not satisfied during ramp.")
            self.set_current(intermediate)
            time.sleep(dt)
        self.set_current(target_amps)

    def shutdown(self):
        self.ramp_current(0.0)

    def get_status(self):
        return {
            'current_amps': self.get_current(),
            'field_T': self.get_field(),
            'interlock_ok': self.interlock_ok(),
            'temperature_ok': self.temperature_ok(),
            'power_supply_enabled': self.power_supply_enabled()
        }

    def close(self):
        self.ao.current_task.close()
        self.ai.current_task.close()
        self.ai.field_task.close()
        self.di.interlock_task.close()
        self.di.temp_ok_task.close()
        self.di.ps_enabled_task.close()
        self.do.control_task.close()
