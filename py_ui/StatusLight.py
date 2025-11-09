from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel


class StatusLight(QWidget):
    _status = False
    _warning = False
    signal = Signal()

    def __init__(self, parent : QLabel, true_text = "Ready", false_text = "Not Ready"):
        super().__init__()
        self._parent = parent
        self._true_text = true_text
        self._false_text = false_text
        self._update_value()

    def _update_value(self):
        if self._status and not self._warning:
            self._parent.setText(f"""<p style="color: green;">{self._true_text}</p>""")
        elif self._status and self._warning:
            self._parent.setText(f"""<p style="color: yellow;">{self._true_text}</p>""")
        elif not self._status and not self._warning:
            self._parent.setText(f"""<p style="color: red;">{self._false_text}</p>""")
        elif not self._status and self._warning:
            self._parent.setText(f"""<p style="color: orange;">{self._false_text}</p>""")
        self.signal.emit()

    def _update_value_text(self, text):
        if self._status and not self._warning:
            self._parent.setText(f"""<p style="color: green;">{self._true_text}: {text}</p>""")
        elif self._status and self._warning:
            self._parent.setText(f"""<p style="color: yellow;">{self._true_text}: {text}</p>""")
        elif not self._status and not self._warning:
            self._parent.setText(f"""<p style="color: red;">{self._false_text}: {text}</p>""")
        elif not self._status and self._warning:
            self._parent.setText(f"""<p style="color: orange;">{self._false_text}: {text}</p>""")
        self.signal.emit()

    def get_status(self):
        return self._status

    def get_warning(self):
        return self._warning

    @Slot()
    def set_status(self, status):
        self._status = status
        self._update_value()

    @Slot()
    def set_warning(self, warning, text):
        self._warning = warning
        self._update_value_text(text)

    def set_simple_warning(self, warning):
        self._warning = warning
        self._update_value()

    def set_full_status_text(self, status, warning, text):
        self._status = status
        self._warning = warning
        self._update_value_text(text)

    def set_full_status(self, status, warning):
        self._status = status
        self._warning = warning
        self._update_value()