from PySide6.QtCore import QSize, Qt
from PySide6.QtDesigner import QFormBuilder, QDesignerCustomWidgetInterface
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QColor, QPixmap, QPainter, QFont

class QStatusLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor("red")

    def set_status_color(self, color_name: str):
        """Set status light color."""
        self._color = QColor(color_name)
        self.update()  # trigger repaint

    def paint_event(self, event):
        """Custom paint event to draw the light."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.GlobalColor.blue)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(QFont("Arial", 30))
        #painter.drawText(rect(), Qt.AlignmentFlag.AlignCenter, "Qt")
        size = min(self.width(), self.height()) - 4

        painter.setBrush(self._color)
        painter.drawEllipse(2, 2, size, size)

    def size_hint(self):
        return QSize(20, 20)
