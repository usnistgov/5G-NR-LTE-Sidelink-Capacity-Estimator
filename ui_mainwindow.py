# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main-window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtCharts import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1242, 776)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayoutFormSubmit = QVBoxLayout()
        self.verticalLayoutFormSubmit.setObjectName(u"verticalLayoutFormSubmit")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblMode = QLabel(self.centralwidget)
        self.lblMode.setObjectName(u"lblMode")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblMode)

        self.comboBoxMode = QComboBox(self.centralwidget)
        self.comboBoxMode.setObjectName(u"comboBoxMode")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBoxMode)

        self.lblMaxQm = QLabel(self.centralwidget)
        self.lblMaxQm.setObjectName(u"lblMaxQm")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblMaxQm)

        self.comboBoxMaxQm = QComboBox(self.centralwidget)
        self.comboBoxMaxQm.setObjectName(u"comboBoxMaxQm")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBoxMaxQm)

        self.lblScalingFactor = QLabel(self.centralwidget)
        self.lblScalingFactor.setObjectName(u"lblScalingFactor")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblScalingFactor)

        self.spinScaleFactor = QSpinBox(self.centralwidget)
        self.spinScaleFactor.setObjectName(u"spinScaleFactor")
        self.spinScaleFactor.setMinimum(1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinScaleFactor)

        self.lblSubchannels = QLabel(self.centralwidget)
        self.lblSubchannels.setObjectName(u"lblSubchannels")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblSubchannels)

        self.spinSubChannels = QSpinBox(self.centralwidget)
        self.spinSubChannels.setObjectName(u"spinSubChannels")
        self.spinSubChannels.setMinimum(1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spinSubChannels)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label)

        self.spinSubchannelSize = QSpinBox(self.centralwidget)
        self.spinSubchannelSize.setObjectName(u"spinSubchannelSize")
        self.spinSubchannelSize.setMaximum(1024)
        self.spinSubchannelSize.setValue(52)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.spinSubchannelSize)


        self.verticalLayoutFormSubmit.addLayout(self.formLayout)

        self.btnCalculate = QPushButton(self.centralwidget)
        self.btnCalculate.setObjectName(u"btnCalculate")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCalculate.sizePolicy().hasHeightForWidth())
        self.btnCalculate.setSizePolicy(sizePolicy)

        self.verticalLayoutFormSubmit.addWidget(self.btnCalculate)


        self.horizontalLayout.addLayout(self.verticalLayoutFormSubmit)

        self.tableResult = QTableView(self.centralwidget)
        self.tableResult.setObjectName(u"tableResult")
        self.tableResult.horizontalHeader().setVisible(True)

        self.horizontalLayout.addWidget(self.tableResult)

        self.verticalLayoutChart = QVBoxLayout()
        self.verticalLayoutChart.setObjectName(u"verticalLayoutChart")
        self.chartView = QtCharts.QChartView(self.centralwidget)
        self.chartView.setObjectName(u"chartView")

        self.verticalLayoutChart.addWidget(self.chartView)


        self.horizontalLayout.addLayout(self.verticalLayoutChart)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1242, 27))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sidelink Capacity Tool", None))
        self.lblMode.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.lblMaxQm.setText(QCoreApplication.translate("MainWindow", u"Max QM", None))
        self.lblScalingFactor.setText(QCoreApplication.translate("MainWindow", u"Scaling Factor", None))
        self.lblSubchannels.setText(QCoreApplication.translate("MainWindow", u"Subchannels", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subchannel Size", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
    # retranslateUi

