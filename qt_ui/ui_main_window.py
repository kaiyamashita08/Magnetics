# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGridLayout,
    QLCDNumber, QLabel, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(722, 533)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.main = QWidget()
        self.main.setObjectName(u"main")
        self.gridLayoutWidget = QWidget(self.main)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(430, 30, 251, 111))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.intfm_status = QLabel(self.gridLayoutWidget)
        self.intfm_status.setObjectName(u"intfm_status")

        self.gridLayout.addWidget(self.intfm_status, 3, 2, 1, 1)

        self.main_status = QLabel(self.gridLayoutWidget)
        self.main_status.setObjectName(u"main_status")

        self.gridLayout.addWidget(self.main_status, 0, 2, 1, 1)

        self.text_3 = QLabel(self.gridLayoutWidget)
        self.text_3.setObjectName(u"text_3")

        self.gridLayout.addWidget(self.text_3, 3, 0, 1, 1)

        self.text = QLabel(self.gridLayoutWidget)
        self.text.setObjectName(u"text")

        self.gridLayout.addWidget(self.text, 2, 0, 1, 1)

        self.text_4 = QLabel(self.gridLayoutWidget)
        self.text_4.setObjectName(u"text_4")

        self.gridLayout.addWidget(self.text_4, 4, 0, 1, 1)

        self.magnet_status = QLabel(self.gridLayoutWidget)
        self.magnet_status.setObjectName(u"magnet_status")

        self.gridLayout.addWidget(self.magnet_status, 2, 2, 1, 1)

        self.stage_status = QLabel(self.gridLayoutWidget)
        self.stage_status.setObjectName(u"stage_status")

        self.gridLayout.addWidget(self.stage_status, 4, 2, 1, 1)

        self.text_2 = QLabel(self.gridLayoutWidget)
        self.text_2.setObjectName(u"text_2")

        self.gridLayout.addWidget(self.text_2, 0, 0, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.main)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(420, 240, 253, 114))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.text_5 = QLabel(self.gridLayoutWidget_2)
        self.text_5.setObjectName(u"text_5")

        self.gridLayout_2.addWidget(self.text_5, 3, 0, 1, 1)

        self.stage_res = QSpinBox(self.gridLayoutWidget_2)
        self.stage_res.setObjectName(u"stage_res")
        self.stage_res.setMaximum(100)
        self.stage_res.setValue(1)

        self.gridLayout_2.addWidget(self.stage_res, 3, 1, 1, 1)

        self.main_start = QPushButton(self.gridLayoutWidget_2)
        self.main_start.setObjectName(u"main_start")

        self.gridLayout_2.addWidget(self.main_start, 4, 1, 1, 1)

        self.text_6 = QLabel(self.gridLayoutWidget_2)
        self.text_6.setObjectName(u"text_6")

        self.gridLayout_2.addWidget(self.text_6, 0, 0, 1, 1)

        self.magnet_strength = QDoubleSpinBox(self.gridLayoutWidget_2)
        self.magnet_strength.setObjectName(u"magnet_strength")

        self.gridLayout_2.addWidget(self.magnet_strength, 0, 1, 1, 1)

        self.magnet_enabled = QCheckBox(self.gridLayoutWidget_2)
        self.magnet_enabled.setObjectName(u"magnet_enabled")
        self.magnet_enabled.setTristate(False)

        self.gridLayout_2.addWidget(self.magnet_enabled, 1, 1, 1, 1)

        self.gridLayoutWidget_3 = QWidget(self.main)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 20, 394, 166))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stage_corner2 = QLabel(self.gridLayoutWidget_3)
        self.stage_corner2.setObjectName(u"stage_corner2")

        self.gridLayout_3.addWidget(self.stage_corner2, 5, 2, 1, 1)

        self.stage_set_corner2 = QPushButton(self.gridLayoutWidget_3)
        self.stage_set_corner2.setObjectName(u"stage_set_corner2")

        self.gridLayout_3.addWidget(self.stage_set_corner2, 6, 1, 1, 1)

        self.text_11 = QLabel(self.gridLayoutWidget_3)
        self.text_11.setObjectName(u"text_11")

        self.gridLayout_3.addWidget(self.text_11, 5, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 4, 7, 1, 1)

        self.stage_set_corner1 = QPushButton(self.gridLayoutWidget_3)
        self.stage_set_corner1.setObjectName(u"stage_set_corner1")

        self.gridLayout_3.addWidget(self.stage_set_corner1, 4, 1, 1, 1)

        self.stage_up = QPushButton(self.gridLayoutWidget_3)
        self.stage_up.setObjectName(u"stage_up")

        self.gridLayout_3.addWidget(self.stage_up, 4, 5, 1, 1)

        self.stage_y = QLCDNumber(self.gridLayoutWidget_3)
        self.stage_y.setObjectName(u"stage_y")

        self.gridLayout_3.addWidget(self.stage_y, 3, 5, 1, 1)

        self.stage_left = QPushButton(self.gridLayoutWidget_3)
        self.stage_left.setObjectName(u"stage_left")

        self.gridLayout_3.addWidget(self.stage_left, 5, 3, 1, 1)

        self.text_7 = QLabel(self.gridLayoutWidget_3)
        self.text_7.setObjectName(u"text_7")

        self.gridLayout_3.addWidget(self.text_7, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 4, 3, 1, 1)

        self.stage_right = QPushButton(self.gridLayoutWidget_3)
        self.stage_right.setObjectName(u"stage_right")

        self.gridLayout_3.addWidget(self.stage_right, 5, 7, 1, 1)

        self.stage_stepsize = QSpinBox(self.gridLayoutWidget_3)
        self.stage_stepsize.setObjectName(u"stage_stepsize")
        self.stage_stepsize.setMaximum(5000)
        self.stage_stepsize.setSingleStep(50)
        self.stage_stepsize.setValue(1000)

        self.gridLayout_3.addWidget(self.stage_stepsize, 3, 7, 1, 1)

        self.text_10 = QLabel(self.gridLayoutWidget_3)
        self.text_10.setObjectName(u"text_10")

        self.gridLayout_3.addWidget(self.text_10, 3, 1, 1, 1)

        self.text_9 = QLabel(self.gridLayoutWidget_3)
        self.text_9.setObjectName(u"text_9")

        self.gridLayout_3.addWidget(self.text_9, 0, 7, 1, 1)

        self.stage_down = QPushButton(self.gridLayoutWidget_3)
        self.stage_down.setObjectName(u"stage_down")

        self.gridLayout_3.addWidget(self.stage_down, 6, 5, 1, 1)

        self.stage_corner1 = QLabel(self.gridLayoutWidget_3)
        self.stage_corner1.setObjectName(u"stage_corner1")

        self.gridLayout_3.addWidget(self.stage_corner1, 3, 2, 1, 1)

        self.text_8 = QLabel(self.gridLayoutWidget_3)
        self.text_8.setObjectName(u"text_8")

        self.gridLayout_3.addWidget(self.text_8, 0, 5, 1, 1)

        self.stage_x = QLCDNumber(self.gridLayoutWidget_3)
        self.stage_x.setObjectName(u"stage_x")

        self.gridLayout_3.addWidget(self.stage_x, 3, 3, 1, 1)

        self.progressbar = QProgressBar(self.main)
        self.progressbar.setObjectName(u"progressbar")
        self.progressbar.setGeometry(QRect(10, 400, 641, 23))
        self.progressbar.setValue(24)
        self.enabled = QCheckBox(self.main)
        self.enabled.setObjectName(u"enabled")
        self.enabled.setGeometry(QRect(50, 270, 78, 20))
        self.tabWidget.addTab(self.main, "")
        self.magnet = QWidget()
        self.magnet.setObjectName(u"magnet")
        self.tabWidget.addTab(self.magnet, "")
        self.interferometer = QWidget()
        self.interferometer.setObjectName(u"interferometer")
        self.tabWidget.addTab(self.interferometer, "")
        self.stage = QWidget()
        self.stage.setObjectName(u"stage")
        self.tabWidget.addTab(self.stage, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 722, 33))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.intfm_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.main_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.text_3.setText(QCoreApplication.translate("MainWindow", u"Interferometer Status", None))
        self.text.setText(QCoreApplication.translate("MainWindow", u"Magnet Status", None))
        self.text_4.setText(QCoreApplication.translate("MainWindow", u"Stage Status", None))
        self.magnet_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.stage_status.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.text_2.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.text_5.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.stage_res.setSuffix(QCoreApplication.translate("MainWindow", u" \u00b5m", None))
        self.main_start.setText(QCoreApplication.translate("MainWindow", u"Start!", None))
        self.text_6.setText(QCoreApplication.translate("MainWindow", u"Magnet Strength", None))
        self.magnet_strength.setSuffix(QCoreApplication.translate("MainWindow", u" T", None))
        self.magnet_enabled.setText(QCoreApplication.translate("MainWindow", u"Enable Magnet", None))
        self.stage_corner2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.stage_set_corner2.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.text_11.setText(QCoreApplication.translate("MainWindow", u"Second Corner", None))
        self.stage_set_corner1.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.stage_up.setText(QCoreApplication.translate("MainWindow", u"Up", None))
        self.stage_left.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.text_7.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.stage_right.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.text_10.setText(QCoreApplication.translate("MainWindow", u"First Corner", None))
        self.text_9.setText(QCoreApplication.translate("MainWindow", u"Microns per Step", None))
        self.stage_down.setText(QCoreApplication.translate("MainWindow", u"Down", None))
        self.stage_corner1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.text_8.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.enabled.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main), QCoreApplication.translate("MainWindow", u"Main", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.magnet), QCoreApplication.translate("MainWindow", u"Magnet", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.interferometer), QCoreApplication.translate("MainWindow", u"Interferometer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stage), QCoreApplication.translate("MainWindow", u"Stage", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

