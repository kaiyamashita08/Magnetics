from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QLCDNumber, QWidget


class PeriodicDisplay(QWidget):
    def __init__(self, parent : QLCDNumber, function, period = 500):
        super().__init__()
        self._function = function
        self._parent = parent
        self.timer = QTimer()
        self.timer.start(period)
        self.timer.timeout.connect(self.update_value)

    @Slot()
    def update_value(self):
        self._parent.display(self._function())