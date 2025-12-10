# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rwr_window_tooldAzIHr.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QTextBrowser,
    QWidget)

class Ui_ToolWindow(object):
    def setupUi(self, ToolWindow):
        if not ToolWindow.objectName():
            ToolWindow.setObjectName("ToolWindow")
        ToolWindow.resize(360, 158)
        self.gridLayout_2 = QGridLayout(ToolWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fullscreenLabel = QLabel(ToolWindow)
        self.fullscreenLabel.setObjectName("fullscreenLabel")

        self.horizontalLayout_2.addWidget(self.fullscreenLabel)

        self.resolutionLabel = QLabel(ToolWindow)
        self.resolutionLabel.setObjectName("resolutionLabel")

        self.horizontalLayout_2.addWidget(self.resolutionLabel)


        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 1, 1, 2)

        self.textBrowser = QTextBrowser(ToolWindow)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout.addWidget(self.textBrowser, 5, 1, 1, 2)

        self.borderlessRadioButton = QRadioButton(ToolWindow)
        self.borderlessRadioButton.setObjectName("borderlessRadioButton")
        self.borderlessRadioButton.setChecked(True)

        self.gridLayout.addWidget(self.borderlessRadioButton, 6, 1, 1, 1)

        self.windowRadioButton = QRadioButton(ToolWindow)
        self.windowRadioButton.setObjectName("windowRadioButton")

        self.gridLayout.addWidget(self.windowRadioButton, 6, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rwrConfigureButton = QPushButton(ToolWindow)
        self.rwrConfigureButton.setObjectName("rwrConfigureButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rwrConfigureButton.sizePolicy().hasHeightForWidth())
        self.rwrConfigureButton.setSizePolicy(sizePolicy)
        self.rwrConfigureButton.setMinimumSize(QSize(0, 0))
        self.rwrConfigureButton.setBaseSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.rwrConfigureButton)

        self.rwrStartButton = QPushButton(ToolWindow)
        self.rwrStartButton.setObjectName("rwrStartButton")

        self.horizontalLayout.addWidget(self.rwrStartButton)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(ToolWindow)

        QMetaObject.connectSlotsByName(ToolWindow)
    # setupUi

    def retranslateUi(self, ToolWindow):
        ToolWindow.setWindowTitle(QCoreApplication.translate("ToolWindow", "RWR Window Tool", None))
        self.fullscreenLabel.setText(QCoreApplication.translate("ToolWindow", "Fullscreen: ", None))
        self.resolutionLabel.setText(QCoreApplication.translate("ToolWindow", "Resolution: ", None))
        self.textBrowser.setHtml(QCoreApplication.translate("ToolWindow", "Reading game graphics settings...", None))
        self.borderlessRadioButton.setText(QCoreApplication.translate("ToolWindow", "Borderless fullscreen", None))
        self.windowRadioButton.setText(QCoreApplication.translate("ToolWindow", "Better window", None))
        self.rwrConfigureButton.setText(QCoreApplication.translate("ToolWindow", "RWR Configure", None))
        self.rwrStartButton.setText(QCoreApplication.translate("ToolWindow", "Start RWR", None))
    # retranslateUi

