from PySide6.QtCore import QObject, Signal, Property
from PySide6.QtWidgets import QWidget, QDoubleSpinBox


class SpinBoxModel(QObject):
    valueChanged = Signal(float)
    
    def __init__(self, defaultValue = 0, parent=None):
        super(SpinBoxModel, self).__init__(parent)
        self._content = defaultValue

    @Property(float, notify=valueChanged)
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

class SyncedSpinBox(QWidget):
    def __init__(self, model, gui_model : QDoubleSpinBox):
        super().__init__()
        self.model = model
        self.gui_model = gui_model
        self.gui_model.setValue(self.model.value)
        self.gui_model.valueChanged.connect(self.model.set_value)
        self.model.valueChanged.connect(self.gui_model.setValue)