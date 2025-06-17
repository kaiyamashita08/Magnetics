import time
from test1 import GMW5972

controller = GMW5972("Dev2")

#print(f"Field: {controller.get_field()}")
print(f"Magnet Flow Interlock: {controller.magnet_flow_interlock()}")
print(f"Magnet Temperature Interlock: {controller.temperature_interlock()}")
print(f"General Interlock: {controller.general_interlock()}")
print(f"EPO trip Interlock: {controller.epo_trip_interlock()}")
print(f"Power Supply Enabled: {controller.power_supply_enabled()}")
controller.set_lockout(True)
for x in range(10):
    print(f"Current: {controller.get_current()}")
    time.sleep(0.1)
controller.set_current(7)
time.sleep(5)
for x in range(10):
    print(f"Current: {controller.get_current()}")
    time.sleep(0.1)
controller.set_current(0)
controller.set_lockout(False)
controller.close()