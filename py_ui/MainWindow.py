import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from py_ui.slots import Slots
from qt_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.slots = Slots()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def only_if_enabled(self, val):
        return val if self.ui.enabled.isChecked() else 0

    def configure_bindings(self):
        # Magnet
        update_magnet = self.slots.start_magnet(
            self.ui.magnet_strength.value() if self.ui.magnet_enabled.isChecked() and self.ui.enabled.isChecked() else 0
        )
        self.ui.magnet_strength.valueChanged.connect(update_magnet)
        self.ui.magnet_enabled.checkStateChanged.connect(update_magnet)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.configure_bindings()

    sys.exit(app.exec())