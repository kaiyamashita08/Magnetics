import sys

from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from py_ui.SyncedCheckBox import CheckBoxModel, SyncedCheckBox
from py_ui.SyncedSpinBox import SpinBoxModel, SyncedSpinBox
from py_ui.Commands import Commands
from qt_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    calibrated = False

    def __init__(self):
        super(MainWindow, self).__init__()
        self.commands = Commands()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.configure_synced_widgets()
        self.timer = QTimer()
        self.timer.start(500)

    def only_if_enabled(self, val):
        return val if self.ui.enabled.isChecked() else 0

    @Slot()
    def update_magnet(self):
        if self.enable_magnet_model.value:
            strength = self.magnet_strength_model.value
        else:
            strength = 0
        self.commands.set_magnet(strength)

    @Slot()
    def update_magnet_display(self):
        field_value = self.commands.get_magnet_field()
        self.ui.magnet_output.display(field_value)

    @Slot()
    def calibrate_magnet(self):
        if self.enable_magnet_model.value:
            val = self.commands.calibrate_magent()
            self.ui.calibration_value.setNum(val)
            if (abs(val) > 30 or abs(val) < 5):
                self.ui.magnet_calibrated.setText("Warning: Check Magnet Sensor")
            else:
                self.ui.magnet_calibrated.setText("Calibrated")
            self.calibrated = True
        else:
            self.ui.calibration_value.setText("Enable Magnet")
        self.update_magnet()

    @Slot()
    def update_magnet_enabled(self, enabled):
        self.ui.magnet_enabled_status.setText(f"{enabled}")

    def configure_synced_widgets(self):
        # Magnet
        self.magnet_strength_model = SpinBoxModel()
        self.ui.magnet_strength_1 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_1)
        self.ui.magnet_strength_2 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_2)

        self.enable_magnet_model = CheckBoxModel()
        self.ui.magnet_enabled_1 = SyncedCheckBox(self.enable_magnet_model, self.ui.magnet_enabled_1)
        self.ui.magnet_enabled_2 = SyncedCheckBox(self.enable_magnet_model, self.ui.magnet_enabled_2)

    def configure_bindings(self):
        # Magnet
        self.enable_magnet_model.valueChanged.connect(self.commands.set_lockout)
        self.magnet_strength_model.valueChanged.connect(self.update_magnet)
        self.enable_magnet_model.valueChanged.connect(self.update_magnet)
        self.enable_magnet_model.valueChanged.connect(self.update_magnet_enabled)
        self.ui.enabled.checkStateChanged.connect(self.update_magnet)
        self.ui.calibrate_button.clicked.connect(self.calibrate_magnet)
        self.timer.timeout.connect(self.update_magnet_display)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.configure_bindings()

    sys.exit(app.exec())