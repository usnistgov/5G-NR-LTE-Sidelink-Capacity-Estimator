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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1028, 698)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabNr = QWidget()
        self.tabNr.setObjectName(u"tabNr")
        self.horizontalLayout = QHBoxLayout(self.tabNr)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblNumerology = QLabel(self.tabNr)
        self.lblNumerology.setObjectName(u"lblNumerology")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblNumerology)

        self.comboNumerology = QComboBox(self.tabNr)
        self.comboNumerology.setObjectName(u"comboNumerology")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboNumerology)

        self.lblResourceBlocks = QLabel(self.tabNr)
        self.lblResourceBlocks.setObjectName(u"lblResourceBlocks")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblResourceBlocks)

        self.spinResourceBlocksNr = QSpinBox(self.tabNr)
        self.spinResourceBlocksNr.setObjectName(u"spinResourceBlocksNr")
        self.spinResourceBlocksNr.setMinimum(11)
        self.spinResourceBlocksNr.setMaximum(52)
        self.spinResourceBlocksNr.setValue(52)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinResourceBlocksNr)

        self.lblLayers = QLabel(self.tabNr)
        self.lblLayers.setObjectName(u"lblLayers")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblLayers)

        self.comboLayers = QComboBox(self.tabNr)
        self.comboLayers.setObjectName(u"comboLayers")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboLayers)

        self.lblModulation = QLabel(self.tabNr)
        self.lblModulation.setObjectName(u"lblModulation")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblModulation)

        self.comboModulation = QComboBox(self.tabNr)
        self.comboModulation.setObjectName(u"comboModulation")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboModulation)

        self.lblHarq = QLabel(self.tabNr)
        self.lblHarq.setObjectName(u"lblHarq")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblHarq)

        self.comboHarq = QComboBox(self.tabNr)
        self.comboHarq.setObjectName(u"comboHarq")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboHarq)

        self.lblBlindTransmissions = QLabel(self.tabNr)
        self.lblBlindTransmissions.setObjectName(u"lblBlindTransmissions")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblBlindTransmissions)

        self.spinBlindTransmissions = QSpinBox(self.tabNr)
        self.spinBlindTransmissions.setObjectName(u"spinBlindTransmissions")
        self.spinBlindTransmissions.setMinimum(1)
        self.spinBlindTransmissions.setMaximum(32)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.spinBlindTransmissions)

        self.lblFeedbackChannel = QLabel(self.tabNr)
        self.lblFeedbackChannel.setObjectName(u"lblFeedbackChannel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lblFeedbackChannel)

        self.comboFeedbackChannel = QComboBox(self.tabNr)
        self.comboFeedbackChannel.setObjectName(u"comboFeedbackChannel")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.comboFeedbackChannel)


        self.verticalLayout.addLayout(self.formLayout)

        self.btnCalculate = QPushButton(self.tabNr)
        self.btnCalculate.setObjectName(u"btnCalculate")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCalculate.sizePolicy().hasHeightForWidth())
        self.btnCalculate.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.btnCalculate)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableResult = QTableView(self.tabNr)
        self.tableResult.setObjectName(u"tableResult")
        self.tableResult.horizontalHeader().setVisible(True)

        self.verticalLayout_4.addWidget(self.tableResult)

        self.btnToggleOverhead = QPushButton(self.tabNr)
        self.btnToggleOverhead.setObjectName(u"btnToggleOverhead")

        self.verticalLayout_4.addWidget(self.btnToggleOverhead)

        self.tableOverHead = QTableView(self.tabNr)
        self.tableOverHead.setObjectName(u"tableOverHead")

        self.verticalLayout_4.addWidget(self.tableOverHead)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tabNr, "")
        self.tabLte = QWidget()
        self.tabLte.setObjectName(u"tabLte")
        self.horizontalLayout_3 = QHBoxLayout(self.tabLte)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lblMcs = QLabel(self.tabLte)
        self.lblMcs.setObjectName(u"lblMcs")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lblMcs)

        self.spinMcs = QSpinBox(self.tabLte)
        self.spinMcs.setObjectName(u"spinMcs")
        self.spinMcs.setMaximum(20)
        self.spinMcs.setValue(20)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.spinMcs)

        self.lblResourceBlocks_2 = QLabel(self.tabLte)
        self.lblResourceBlocks_2.setObjectName(u"lblResourceBlocks_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lblResourceBlocks_2)

        self.spinResourceBlocksLte = QSpinBox(self.tabLte)
        self.spinResourceBlocksLte.setObjectName(u"spinResourceBlocksLte")
        self.spinResourceBlocksLte.setMinimum(1)
        self.spinResourceBlocksLte.setMaximum(128)
        self.spinResourceBlocksLte.setValue(50)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.spinResourceBlocksLte)

        self.label = QLabel(self.tabLte)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label)

        self.spinPeriodSize = QSpinBox(self.tabLte)
        self.spinPeriodSize.setObjectName(u"spinPeriodSize")
        self.spinPeriodSize.setMaximum(320)
        self.spinPeriodSize.setValue(40)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.spinPeriodSize)

        self.label_2 = QLabel(self.tabLte)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.spinPscchSize = QSpinBox(self.tabLte)
        self.spinPscchSize.setObjectName(u"spinPscchSize")
        self.spinPscchSize.setMinimum(2)
        self.spinPscchSize.setMaximum(40)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.spinPscchSize)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.btnCalculateLte = QPushButton(self.tabLte)
        self.btnCalculateLte.setObjectName(u"btnCalculateLte")
        sizePolicy.setHeightForWidth(self.btnCalculateLte.sizePolicy().hasHeightForWidth())
        self.btnCalculateLte.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.btnCalculateLte)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.tableResultLte = QTableView(self.tabLte)
        self.tableResultLte.setObjectName(u"tableResultLte")

        self.horizontalLayout_3.addWidget(self.tableResultLte)

        self.tabWidget.addTab(self.tabLte, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1028, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sidelink Capacity Tool", None))
        self.lblNumerology.setText(QCoreApplication.translate("MainWindow", u"Numerology", None))
        self.lblResourceBlocks.setText(QCoreApplication.translate("MainWindow", u"Resource Blocks", None))
        self.spinResourceBlocksNr.setSuffix(QCoreApplication.translate("MainWindow", u"PRB", None))
        self.lblLayers.setText(QCoreApplication.translate("MainWindow", u"Layers", None))
        self.lblModulation.setText(QCoreApplication.translate("MainWindow", u"Max Modulation", None))
        self.lblHarq.setText(QCoreApplication.translate("MainWindow", u"HARQ Mode", None))
        self.lblBlindTransmissions.setText(QCoreApplication.translate("MainWindow", u"Blind Transmissions", None))
        self.lblFeedbackChannel.setText(QCoreApplication.translate("MainWindow", u"Feedback Channel Period", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
        self.btnToggleOverhead.setText(QCoreApplication.translate("MainWindow", u"\u2b9f Toggle Overhead Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNr), QCoreApplication.translate("MainWindow", u"NR", None))
        self.lblMcs.setText(QCoreApplication.translate("MainWindow", u"MCS", None))
        self.lblResourceBlocks_2.setText(QCoreApplication.translate("MainWindow", u"Resource Blocks", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Period Size", None))
        self.spinPeriodSize.setSuffix(QCoreApplication.translate("MainWindow", u" Subframes", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Control Channel Size", None))
        self.spinPscchSize.setSuffix(QCoreApplication.translate("MainWindow", u" Subframes", None))
        self.btnCalculateLte.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLte), QCoreApplication.translate("MainWindow", u"LTE", None))
    # retranslateUi

