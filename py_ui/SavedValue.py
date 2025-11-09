from PySide6.QtCore import Property, Signal
from PySide6.QtWidgets import QWidget, QLabel


class SavedValue(QWidget):
    valueChanged = Signal(object)

    def __init__(self, parent : QLabel, value = None):
        super().__init__()
        self._parent = parent
        self._value = value
        self._initialized = value is not None
        self._parent.setText(f"{value}")

    @Property(object, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._content:
            print(f"setting value: {new_value}")
            self._value = new_value
            self.valueChanged.emit(new_value)

    def set_value(self, value):
        self.value = value
        self._parent.setText(f"{value}")
        self._initialized = True

    def value_defined(self):
        return self._initialized

    def get_value(self):
        if not self._initialized:
            raise ReferenceError
        else:
            return self._value