import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from py_ui.SyncedSpinBox import SpinBoxModel, SyncedSpinBox
from py_ui.slots import Slots
from qt_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    # Signals must be declared as class attributes
    update_magnet_signal = Signal()
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.slots = Slots()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.configure_synced_widgets()

    def only_if_enabled(self, val):
        return val if self.ui.enabled.isChecked() else 0

    @Slot()
    def update_magnet(self):
        if self.ui.magnet_enabled.isChecked() and self.ui.enabled.isChecked():
            strength = self.magnet_strength_model.value
        else:
            strength = 0
        self.slots.start_magnet(strength)

    def configure_synced_widgets(self):
        # Magnet
        self.magnet_strength_model = SpinBoxModel()
        self.ui.magnet_strength_1 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_1)
        self.ui.magnet_strength_2 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_2)

    def configure_bindings(self):
        # Magnet
        self.update_magnet_signal.connect(self.update_magnet)
        
        self.magnet_strength_model.valueChanged.connect(self.update_magnet_signal)
        self.ui.magnet_enabled.checkStateChanged.connect(self.update_magnet_signal)
        self.ui.enabled.checkStateChanged.connect(self.update_magnet_signal)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.configure_bindings()

    sys.exit(app.exec())