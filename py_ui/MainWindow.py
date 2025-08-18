import sys

from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from py_ui.PeriodicDisplay import PeriodicDisplay
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
        """
        Synced Widgets
        """
        # Magnet
        self.magnet_strength_model = SpinBoxModel()
        self.ui.magnet_strength_1 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_1)
        self.ui.magnet_strength_2 = SyncedSpinBox(self.magnet_strength_model, self.ui.magnet_strength_2)

        self.enable_magnet_model = CheckBoxModel()
        self.ui.magnet_enabled_1 = SyncedCheckBox(self.enable_magnet_model, self.ui.magnet_enabled_1)
        self.ui.magnet_enabled_2 = SyncedCheckBox(self.enable_magnet_model, self.ui.magnet_enabled_2)

        # Stage
        self.step_size_model = SpinBoxModel()
        self.ui.stage_stepsize = SyncedSpinBox(self.step_size_model, self.ui.stage_stepsize)
        self.ui.stage_stepsize_2 = SyncedSpinBox(self.step_size_model, self.ui.stage_stepsize_2)
        """
        Periodic Displays
        """
        self.ui.magnet_output = PeriodicDisplay(self.ui.magnet_output, self.commands.get_magnet_field)
        self.ui.stage_x = PeriodicDisplay(self.ui.stage_x, self.commands.get_x)
        self.ui.stage_x_2 = PeriodicDisplay(self.ui.stage_x_2, self.commands.get_x)
        self.ui.stage_y = PeriodicDisplay(self.ui.stage_y, self.commands.get_y)
        self.ui.stage_y_2 = PeriodicDisplay(self.ui.stage_y_2, self.commands.get_y)

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

    @Slot()
    def save_data(self):
        self.commands.save_data("TODO")

    @Slot()
    def stage_up(self):
        self.commands.move_xy_relative(0, self.step_size_model.get_value())
    @Slot()
    def stage_right(self):
        self.commands.move_xy_relative(self.step_size_model.get_value(), 0)
    @Slot()
    def stage_down(self):
        self.commands.move_xy_relative(0, -1 * self.step_size_model.get_value())
    @Slot()
    def stage_left(self):
        self.commands.move_xy_relative(-1 * self.step_size_model.get_value(), 0)

    def configure_bindings(self):
        # Magnet
        self.enable_magnet_model.valueChanged.connect(self.commands.set_lockout)
        self.magnet_strength_model.valueChanged.connect(self.update_magnet)
        self.enable_magnet_model.valueChanged.connect(self.update_magnet)
        self.enable_magnet_model.valueChanged.connect(self.update_magnet_enabled)
        self.ui.enabled.checkStateChanged.connect(self.update_magnet)
        self.ui.calibrate_button.clicked.connect(self.calibrate_magnet)

        # Interferometer
        self.ui.save_data.clicked.connect(self.save_data)

        # Stage
        self.ui.stage_up.clicked.connect(self.stage_up)
        self.ui.stage_up_2.clicked.connect(self.stage_up)
        self.ui.stage_right.clicked.connect(self.stage_right)
        self.ui.stage_right_2.clicked.connect(self.stage_right)
        self.ui.stage_down.clicked.connect(self.stage_down)
        self.ui.stage_down_2.clicked.connect(self.stage_down)
        self.ui.stage_left.clicked.connect(self.stage_left)
        self.ui.stage_left_2.clicked.connect(self.stage_left)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.configure_bindings()

    sys.exit(app.exec())