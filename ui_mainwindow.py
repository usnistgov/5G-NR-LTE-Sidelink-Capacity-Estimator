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
        self.lblNumerology = QLabel(self.centralwidget)
        self.lblNumerology.setObjectName(u"lblNumerology")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblNumerology)

        self.comboNumerology = QComboBox(self.centralwidget)
        self.comboNumerology.setObjectName(u"comboNumerology")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboNumerology)

        self.lblLayers = QLabel(self.centralwidget)
        self.lblLayers.setObjectName(u"lblLayers")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblLayers)

        self.comboLayers = QComboBox(self.centralwidget)
        self.comboLayers.setObjectName(u"comboLayers")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboLayers)

        self.lblModulation = QLabel(self.centralwidget)
        self.lblModulation.setObjectName(u"lblModulation")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblModulation)

        self.comboModulation = QComboBox(self.centralwidget)
        self.comboModulation.setObjectName(u"comboModulation")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboModulation)

        self.lblHarq = QLabel(self.centralwidget)
        self.lblHarq.setObjectName(u"lblHarq")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblHarq)

        self.comboHarq = QComboBox(self.centralwidget)
        self.comboHarq.setObjectName(u"comboHarq")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboHarq)

        self.lblResourceBlocks = QLabel(self.centralwidget)
        self.lblResourceBlocks.setObjectName(u"lblResourceBlocks")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblResourceBlocks)

        self.spinResourceBlocks = QSpinBox(self.centralwidget)
        self.spinResourceBlocks.setObjectName(u"spinResourceBlocks")
        self.spinResourceBlocks.setMinimum(11)
        self.spinResourceBlocks.setMaximum(52)
        self.spinResourceBlocks.setValue(52)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinResourceBlocks)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label)

        self.spinBlindRetransmissions = QSpinBox(self.centralwidget)
        self.spinBlindRetransmissions.setObjectName(u"spinBlindRetransmissions")
        self.spinBlindRetransmissions.setMinimum(1)
        self.spinBlindRetransmissions.setMaximum(32)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.spinBlindRetransmissions)


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
        self.menubar.setGeometry(QRect(0, 0, 1242, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sidelink Capacity Tool", None))
        self.lblNumerology.setText(QCoreApplication.translate("MainWindow", u"Numerology", None))
        self.lblLayers.setText(QCoreApplication.translate("MainWindow", u"Layers", None))
        self.lblModulation.setText(QCoreApplication.translate("MainWindow", u"Max Modulation", None))
        self.lblHarq.setText(QCoreApplication.translate("MainWindow", u"HARQ Mode", None))
        self.lblResourceBlocks.setText(QCoreApplication.translate("MainWindow", u"Resource Blocks", None))
        self.spinResourceBlocks.setSuffix(QCoreApplication.translate("MainWindow", u"PRB", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Blind Transmissions", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
    # retranslateUi

