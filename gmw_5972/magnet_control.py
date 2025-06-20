import time

from gmw_5972.gmw_5972 import GMW5972


class magnet_control:
    lockout = False

    def __init__(self, current_per_T = 21.8, max_current = 60):
        self.gmw5972 = GMW5972()
        self.current_per_T = current_per_T
        self.max_current = max_current

    def get_lockout(self):
        return self.lockout

    def get_current_per_T(self):
        return self.current_per_T

    def get_field(self):
        return self.gmw5972.get_field()

    def set_lockout(self, state):
        self.gmw5972.set_lockout(state)
        self.lockout = state
        self.set_current(0)

    def set_current(self, current):
        if self.lockout:
            self.gmw5972.set_current(current)
        else:
            self.gmw5972.set_current(0)

    def calibrate_magnet(self):
        if self.lockout:
            self.set_current(5)
            time.sleep(2)
            self.current_per_T = 5 / self.gmw5972.get_field()
            self.set_current(0)
            print(f"Calibrated magnet to {self.current_per_T} amps per tesla")

    def set_magnet(self, teslas):
        self.set_current(teslas * self.current_per_T)

    def close(self):
        self.gmw5972.set_current(0)
        self.gmw5972.set_lockout(False)
        self.gmw5972.close()