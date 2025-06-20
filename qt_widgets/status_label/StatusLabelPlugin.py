from PySide6.QtDesigner import QDesignerCustomWidgetInterface
from PySide6.QtCore import Qt, QObject
from .QStatusLabel import QStatusLabel

class StatusLabelPlugin(QObject, QDesignerCustomWidgetInterface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initialized = False

    # ---- mandatory interface -------------
    def createWidget(self, parent):
        return QStatusLabel(parent)

    def name(self):
        return "QStatusLabel"

    def group(self):
        return "Custom Widgets"

    def toolTip(self):
        return "Round status indicator"

    def whatsThis(self):
        return "Displays a coloured status light (red/green/…)."

    def isContainer(self):
        return False

    def includeFile(self):
        # module that Designer adds to generated .py
        return "statuslabel"

    # ---- optional helpers -------------
    def icon(self):
        # could return a custom QIcon
        return super().icon()

    def isInitialized(self):
        return self._initialized

    def initialize(self, core):
        if self._initialized:
            return
        self._initialized = True