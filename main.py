import time

from gmw_5972.magnet_control import magnet_control
from proscan_stage.Stage import Stage

"""
controller = magnet_control()

controller.set_lockout(True)
controller.calibrate_magnet()
controller.set_magnet(0.3)
time.sleep(0.4)
print(controller.get_field())
controller.close()
"""

stage = Stage()
stage.set_position(0,0)
stage.go_to_pos(5000, 5000)
while stage.busy():
    print("waiting")
    time.sleep(0.2)
print(stage.busy())