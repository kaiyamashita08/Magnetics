import time

from py_ui.Commands import Commands

commands = Commands()

commands.set_lockout(True)
time.sleep(0.2)
print(commands.ready())
print(commands.run(10000, 10000, 2000, 2000, 0, 0, 0.2, 1))

commands.close()