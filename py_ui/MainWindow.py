import sys

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow

from py_ui.PeriodicDisplay import PeriodicDisplay
from py_ui.SavedValue import SavedValue
from py_ui.StatusLight import StatusLight
from py_ui.SyncedCheckBox import CheckBoxModel, SyncedCheckBox
from py_ui.SyncedSavedValue import SyncedSavedValueModel, SyncedSavedValue
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
        self.step_size_model = SpinBoxModel(500.0)
        self.ui.stage_stepsize = SyncedSpinBox(self.step_size_model, self.ui.stage_stepsize)
        self.ui.stage_stepsize_2 = SyncedSpinBox(self.step_size_model, self.ui.stage_stepsize_2)

        self.corner_1_model = SyncedSavedValueModel()
        self.ui.stage_corner1 = SyncedSavedValue(self.corner_1_model, self.ui.stage_corner1)
        self.ui.stage_corner1_2 = SyncedSavedValue(self.corner_1_model, self.ui.stage_corner1_2)
        self.corner_2_model = SyncedSavedValueModel()
        self.ui.stage_corner2 = SyncedSavedValue(self.corner_2_model, self.ui.stage_corner2)
        self.ui.stage_corner2_2 = SyncedSavedValue(self.corner_2_model, self.ui.stage_corner2_2)

        """
        Periodic Displays
        """
        self.ui.magnet_output = PeriodicDisplay(self.ui.magnet_output, self.commands.get_magnet_field)
        self.ui.stage_x = PeriodicDisplay(self.ui.stage_x, self.commands.get_x)
        self.ui.stage_x_2 = PeriodicDisplay(self.ui.stage_x_2, self.commands.get_x)
        self.ui.stage_y = PeriodicDisplay(self.ui.stage_y, self.commands.get_y)
        self.ui.stage_y_2 = PeriodicDisplay(self.ui.stage_y_2, self.commands.get_y)
        """
        Status Lights
        """
        # Magnet
        self.ui.magnet_status_1 = StatusLight(self.ui.magnet_status_1)
        self.ui.magnet_status_2 = StatusLight(self.ui.magnet_status_2)
        self.ui.magnet_enabled_status = StatusLight(self.ui.magnet_enabled_status, "Enabled", "Disabled")
        self.ui.magnet_calibrated = StatusLight(self.ui.magnet_calibrated)
        self.ui.magnet_calibrated.set_status(True)
        self.ui.magnet_calibrated.set_warning(True, "Not Calibrated")
        # Interferometer
        # TODO: Make PeriodicStatusLight?
        self.ui.interferometer_ready = StatusLight(self.ui.interferometer_ready)
        self.ui.intfm_status = StatusLight(self.ui.intfm_status)
        # Stage

    def only_if_enabled(self, val):
        return val if self.ui.enabled.isChecked() else 0

    @Slot()
    def update_magnet(self):
        if self.enable_magnet_model.get_value():
            strength = self.magnet_strength_model.get_value()
        else:
            strength = 0
        self.commands.set_magnet(strength)

    @Slot()
    def calibrate_magnet(self):
        if self.enable_magnet_model.get_value():
            val = self.commands.calibrate_magent()
            self.ui.calibration_value.setNum(val)
            if (abs(val) > 30 or abs(val) < 5):
                self.ui.magnet_calibrated.set_full_status_text(False, True, "Check Magnet Sensor")
            else:
                self.ui.magnet_calibrated.set_full_status(True, False)
            self.calibrated = True
        else:
            self.ui.calibration_value.setText("Enable Magnet")
        self.update_magnet()

    @Slot()
    def update_magnet_enabled(self, enabled):
        self.ui.magnet_enabled_status.set_status(enabled)

    @Slot()
    def save_data(self):
        self.commands.save_data("TODO")

    @Slot()
    def stage_up(self):
        if self.commands.stage_cmd_ready():
            self.commands.move_xy_relative(0, self.step_size_model.get_value())
    @Slot()
    def stage_right(self):
        if self.commands.stage_cmd_ready():
            self.commands.move_xy_relative(self.step_size_model.get_value(), 0)
    @Slot()
    def stage_down(self):
        if self.commands.stage_cmd_ready():
            self.commands.move_xy_relative(0, -1 * self.step_size_model.get_value())
    @Slot()
    def stage_left(self):
        if self.commands.stage_cmd_ready():
            self.commands.move_xy_relative(-1 * self.step_size_model.get_value(), 0)

    @Slot()
    def save_corner_1(self):
        self.corner_1_model.set_value(self.commands.get_position())
    @Slot()
    def save_corner_2(self):
        self.corner_2_model.set_value(self.commands.get_position())

    @Slot()
    def update_magnet_status(self):
        self.ui.magnet_status_1.set_status(self.ui.magnet_calibrated.get_status())
        self.ui.magnet_status_1.set_simple_warning(self.ui.magnet_calibrated.get_warning())
        self.ui.magnet_status_2.set_status(self.ui.magnet_calibrated.get_status())
        self.ui.magnet_status_2.set_simple_warning(self.ui.magnet_calibrated.get_warning())

    @Slot()
    def update_intfm_status(self):
        self.ui.interferometer_ready.set_status(self.commands.interferometer.ready())
        self.ui.intfm_status.set_status(self.commands.interferometer.ready())

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

        self.ui.stage_set_corner1.clicked.connect(self.save_corner_1)
        self.ui.stage_set_corner2.clicked.connect(self.save_corner_2)
        self.ui.stage_set_corner1_2.clicked.connect(self.save_corner_1)
        self.ui.stage_set_corner2_2.clicked.connect(self.save_corner_2)

        """
        Status Lights
        """
        # Magnet
        self.ui.magnet_calibrated.signal.connect(self.update_magnet_status)
        self.update_magnet_status()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.configure_bindings()

    sys.exit(app.exec())