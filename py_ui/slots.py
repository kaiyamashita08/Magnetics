from PySide6.QtCore import Slot

from py_ui.Commands import Commands


class Slots:
    def __init__(self):
        self.flux = 0
        self.commands = Commands()

    @Slot()
    def start_magnet(self):
        self.commands.set_magnet(self.flux)