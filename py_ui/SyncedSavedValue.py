from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel

from py_ui.SavedValue import SavedValue


class SyncedSavedValueModel(QObject):
    valueChanged = Signal(object)

    def __init__(self, defaultValue = None, parent=None):
        super(SyncedSavedValueModel, self).__init__(parent)
        self._content = defaultValue

    @Property(object, notify=valueChanged)
    def value(self):
        return self._content

    @value.setter
    def value(self, new_value):
        if new_value != self._content:
            print(f"setting value: {new_value}")
            self._content = new_value
            self.valueChanged.emit(new_value)

    def set_value(self, new_value):
        self.value = new_value

    def get_value(self):
        return self._content

class SyncedSavedValue(QWidget):
    def __init__(self, model, gui_model : QLabel):
        super().__init__()
        self.model = model
        self.gui_model = gui_model
        self.gui_model.setText(f"{self.model.value}")
        self.model.valueChanged.connect(self.set_text)

    @Slot()
    def set_text(self):
        self.gui_model.setText(f"{self.model.value}")