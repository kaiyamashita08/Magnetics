import time


class Stage:
    """
    A class for a HLD117NN linear stage connected to a Proscan III controller
    This uses the Prior SDK python interface and documentation on commands can be found by downloading the SDK off of the Prior website
    """

    flag = 0
    is_busy = False
    x = 0
    y = 0
    max_speed = 1000
    max_accel = 10000
    max_jerk = 50

    def __init__(self, port = 8, path = r"C:\Users\kaiya\Documents\proscan_stage\PriorScientificSDK.dll"):
        """
        Initialize a linear stage connected to a Proscan III using the Prior python interface
        :param port: The COM port that the Proscan III is connected to. For example, put 8 for COM8
        :param path: The path of the Prior SDK .dll file
        :raise: Multiple different errors if the connection fails
        """

        self.path = path
        self.port = port

        self._set_flag("1")

    def _cmd(self, msg):
        """
        Call a command and get the return value from the SDK
        :param msg: The command to run
        :return: The returned value from the SDK
        :raise API Error: If the return throws an error
        """

    def _set_flag(self, flag):
        """
        Sets the flag on the Proscan controller. This can be used to signify different states of the controller.
        This flag is set to "0" whenever the Proscan restarts
        :param flag: The flag, as a 8-digit long hexadecimal string, e.g. "1" or "ABCD1234"
        """
        self.flag = flag

    def _get_flag(self):
        """
        Gets the flag on the Proscan controller
        :return: The flag as a string
        """
        return self.flag

    def busy(self):
        """
        Returns whether the linear stage is busy
        :return: True if busy, False if ready
        """
        return self.is_busy

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
        return self.x, self.y

    def set_position(self, x, y):
        """
        Sets the position of the stage in microns
        :param x: X position
        :param y: Y position
        """
        self.x = x
        self.y = y

    def go_to_pos(self, x, y):
        """
        Go to an absolute position
        :param x: X position
        :param y: Y position
        """
        self.is_busy = True
        time.sleep(0.3)
        self.x = x
        self.y = y
        self.is_busy = False

    def go_to_pos_relative(self, x, y):
        """
        Go to a relative position
        :param x: X position
        :param y: Y position
        """
        self.is_busy = True
        time.sleep(0.3)
        self.x += x
        self.y += y
        self.is_busy = False

    def move_at_velocity(self, x, y):
        """
        Move at a velocity (in microns per second)
        :param x: X velocity
        :param y: Y velocity
        """
        print(f"Moving at velocity x: {x}, y: {y}")

    def get_steps_per_micron(self):
        """
        Get how many encoder steps per micron. This tells the maximum possible accuracy of the stage
        :return: Encoder steps per micron
        """
        return 25

    def get_max_speed(self):
        """
        The maximum allowed speed of the stage in normal operation
        :return: The maximum speed in microns per second
        """
        return self.max_speed

    def set_max_speed(self, speed):
        """
        Set the maximum allowed speed of the stage
        :param speed: The maximum speed in microns per second
        """
        self.max_speed = speed

    def get_max_acc(self):
        """
        Get the maximum allowed acceleration of the stage
        :return: The maximum acceleration in microns per second squared
        """
        return self.max_accel

    def set_max_acc(self, acc):
        """
        Set the maximum allowed acceleration of the stage
        :param acc: The maximum acceleration in microns per second squared
        """
        self.max_accel = acc

    def get_max_jerk(self):
        """
        Get the minimum allowed jerk time, i.e. the minimum time it takes before maximum acceleration is reached
        :return: The minimum jerk time in milliseconds
        """
        return self.max_jerk

    def set_max_jerk(self, jerk):
        """
        Set the minimum allowed jerk time
        :param jerk: The minimum jerk time in milliseconds
        """
        self.max_jerk = jerk

    def safe_stop(self):
        """
        Smoothly stop the stage and everything else connected to the controller
        """
        print("Stopping smoothly")

    def emergency_stop(self):
        """
        Emergency stop the controller and the stage, ignoring any software limits
        WARNING: This should only be done in emergencies and may lose positional accuracy
        """
        print("Stopping abruptly")

    def close(self):
        """
        Stop the stage and disconnect from the controller
        """
        self.safe_stop()
        print("Closing")