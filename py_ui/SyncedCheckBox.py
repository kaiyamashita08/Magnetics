from PySide6.QtCore import QObject, Signal, Property, Qt, Slot
from PySide6.QtWidgets import QWidget, QCheckBox


class CheckBoxModel(QObject):
    valueChanged = Signal(bool)

    def __init__(self, defaultValue=False, parent=None):
        super(CheckBoxModel, self).__init__(parent)
        self._content = defaultValue

    @Property(bool, notify=valueChanged)
    def value(self):
        return self._content

    @value.setter
    def value(self, new_value):
        if new_value != self._content:
            self._content = new_value
            self.valueChanged.emit(new_value)

    def set_value(self, new_value):
        self.value = new_value


class SyncedCheckBox(QWidget):
    def __init__(self, model, gui_model: QCheckBox):
        super().__init__()
        self.model = model
        self.gui_model = gui_model
        self.gui_model.setChecked(self.model.value)
        self.gui_model.checkStateChanged.connect(self._set_checked)
        self.model.valueChanged.connect(self.gui_model.setChecked)

    @Slot()
    def _set_checked(self, state):
        is_checked = (state == Qt.CheckState.Checked)
        self.model.set_value(is_checked)