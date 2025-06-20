import time
from math import floor

from Interferometer.Interferometer_sim import Interferometer
from gmw_5972.magnet_control import magnet_control
from proscan_stage.Stage import Stage

import numpy as np

class Commands:
    def __init__(self):
        self.magnet_control = magnet_control()
        self.interferometer = Interferometer()
        self.stage = Stage()
        self.magnet_control.calibrate_magnet()

    def ready(self):
        return self.magnet_control.get_lockout() and self.interferometer.ready() and self.stage.cmd_ready()

    def set_lockout(self, state):
        self.magnet_control.set_lockout(state)

    def _wait_until_done_moving(self):
        while self.stage.busy():
            time.sleep(0.2)

    def run(self, xlen, ylen, xres, yres, xstart, ystart, flux, scans = 1):
        if not self.ready():
            return
        xdim = floor(xlen / xres) + 1
        ydim = floor(ylen / yres) + 1
        array = np.zeros([90, ydim, xdim], np.int32)
        self.magnet_control.set_magnet(flux)
        self.stage.go_to_pos(xstart,ystart)
        self._wait_until_done_moving()
        for y in range(ydim):
            for x in range(xdim):
                self.stage.go_to_pos(xstart+xres*x, ystart+yres*y)
                self._wait_until_done_moving()
                data = self.interferometer.make_scans(scans)
                for f in range(90):
                    array[f, y, x] = data[f][1]
            self.stage.go_to_pos(xstart, ystart + y * yres)
        return array

    def close(self):
        self.magnet_control.close()
        self.stage.close()