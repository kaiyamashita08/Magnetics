from ctypes import WinDLL, create_string_buffer
import os

import Util


class Stage:
    """
    A class for a HLD117NN linear stage connected to a Proscan III controller
    This uses the Prior SDK python interface and documentation on commands can be found by downloading the SDK off of the Prior website
    """

    def __init__(self, port = 8, path = r"C:\Users\lab\Documents\GitHub\Magnetics\proscan_stage\PriorScientificSDK.dll"):
        """
        Initialize a linear stage connected to a Proscan III using the Prior python interface
        :param port: The COM port that the Proscan III is connected to. For example, put 8 for COM8
        :param path: The path of the Prior SDK .dll file
        :raise: Multiple different errors if the connection fails
        """

        self.path = path
        self.port = port

        if os.path.exists(self.path):
            self.SDKPrior = WinDLL(self.path)
        else:
            raise RuntimeError("DLL could not be loaded.")

        self.rx = create_string_buffer(1000)

        ret = self.SDKPrior.PriorScientificSDK_Initialise()
        if ret:
            print(f"Error initialising {ret}")
            raise Exception("Initialization Error")
        else:
            print(f"Ok initialising {ret}")

        ret = self.SDKPrior.PriorScientificSDK_Version(self.rx)
        print(f"dll version api ret={ret}, version={self.rx.value.decode()}")

        self.sessionID = self.SDKPrior.PriorScientificSDK_OpenNewSession()
        if self.sessionID < 0:
            print(f"Error getting sessionID {ret}")
            raise Exception("Invalid sessionID")
        else:
            print(f"SessionID = {self.sessionID}")

        self._cmd(f"controller.connect {self.port}")

        self._set_flag("1")

    def _cmd(self, msg):
        """
        Call a command and get the return value from the SDK
        :param msg: The command to run
        :return: The returned value from the SDK
        :raise API Error: If the return throws an error
        """
        ret = self.SDKPrior.PriorScientificSDK_cmd(
            self.sessionID, create_string_buffer(msg.encode()), self.rx
        )
        if ret:
            print(f"Api error {ret}")
            print(self.rx.value.decode())
            raise Exception("API Error")

        return self.rx.value.decode()

    def _set_flag(self, flag):
        """
        Sets the flag on the Proscan controller. This can be used to signify different states of the controller.
        This flag is set to "0" whenever the Proscan restarts
        :param flag: The flag, as a 8-digit long hexadecimal string, e.g. "1" or "ABCD1234"
        """
        self._cmd(f"controller.flag.set {flag}")

    def _get_flag(self):
        """
        Gets the flag on the Proscan controller
        :return: The flag as a string
        """
        return self._cmd(f"controller.flag.get")

    def busy(self):
        """
        Returns whether the linear stage is busy
        :return: True if busy, False if ready
        """
        return self._cmd("controller.stage.busy.get") != "0"

    def cmd_ready(self):
        """
        Returns whether a command is ready, i.e. the controller is fine and the stage is not busy
        :return: True if ready, false if not
        """
        return self._get_flag() != "0" and not self.busy()

    def get_position(self):
        """
        Gets the current XY position of the stage in microns
        :return: The position, in an ordered pair
        """
        return Util.str_to_pair_int(self._cmd("controller.stage.position.get"))

    def set_position(self, x, y):
        """
        Sets the position of the stage in microns
        :param x: X position
        :param y: Y position
        """
        self._cmd(f"controller.stage.position.set {x} {y}")

    def go_to_pos(self, x, y):
        """
        Go to an absolute position
        :param x: X position
        :param y: Y position
        """
        self._cmd(f"controller.stage.goto-position {x} {y}")

    def go_to_pos_relative(self, x, y):
        """
        Go to a relative position
        :param x: X position
        :param y: Y position
        """
        self._cmd(f"controller.stage.move-relative {x} {y}")

    def move_at_velocity(self, x, y):
        """
        Move at a velocity (in microns per second)
        :param x: X velocity
        :param y: Y velocity
        """
        self._cmd(f"controller.stage.move-at-velocity {x} {y}")

    def get_steps_per_micron(self):
        """
        Get how many encoder steps per micron. This tells the maximum possible accuracy of the stage
        :return: Encoder steps per micron
        """
        return int(self._cmd(f"controller.stage.steps-per-micron.get"))

    def get_max_speed(self):
        """
        The maximum allowed speed of the stage in normal operation
        :return: The maximum speed in microns per second
        """
        return int(self._cmd(f"controller.stage.speed.get"))

    def set_max_speed(self, speed):
        """
        Set the maximum allowed speed of the stage
        :param speed: The maximum speed in microns per second
        """
        self._cmd(f"controller.stage.speed.set {speed}")

    def get_max_acc(self):
        """
        Get the maximum allowed acceleration of the stage
        :return: The maximum acceleration in microns per second squared
        """
        return int(self._cmd(f"controller.stage.acc.get"))

    def set_max_acc(self, acc):
        """
        Set the maximum allowed acceleration of the stage
        :param acc: The maximum acceleration in microns per second squared
        """
        self._cmd(f"controller.stage.acc.set {acc}")

    def get_max_jerk(self):
        """
        Get the minimum allowed jerk time, i.e. the minimum time it takes before maximum acceleration is reached
        :return: The minimum jerk time in milliseconds
        """
        return int(self._cmd(f"controller.stage.jerk.get"))

    def set_max_jerk(self, jerk):
        """
        Set the minimum allowed jerk time
        :param jerk: The minimum jerk time in milliseconds
        """
        self._cmd(f"controller.stage.jerk.set {jerk}")

    def safe_stop(self):
        """
        Smoothly stop the stage and everything else connected to the controller
        """
        self._cmd(f"controller.stop.smoothly")

    def emergency_stop(self):
        """
        Emergency stop the controller and the stage, ignoring any software limits
        WARNING: This should only be done in emergencies and may lose positional accuracy
        """
        self._cmd(f"controller.stop.abruptly")

    def close(self):
        """
        Stop the stage and disconnect from the controller
        """
        self.safe_stop()
        self._cmd("controller.disconnect")