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

from PySide2.QtCharts import QtCharts


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1422, 627)
        MainWindow.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}")
        self.action_CSV = QAction(MainWindow)
        self.action_CSV.setObjectName(u"action_CSV")
        self.actionClear_Tables = QAction(MainWindow)
        self.actionClear_Tables.setObjectName(u"actionClear_Tables")
        self.actionDelete_Selected = QAction(MainWindow)
        self.actionDelete_Selected.setObjectName(u"actionDelete_Selected")
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
        self.verticalLayoutInputsNr = QVBoxLayout()
        self.verticalLayoutInputsNr.setObjectName(u"verticalLayoutInputsNr")
        self.lblInputsNr = QLabel(self.tabNr)
        self.lblInputsNr.setObjectName(u"lblInputsNr")
        font = QFont()
        font.setPointSize(18)
        self.lblInputsNr.setFont(font)
        self.lblInputsNr.setAlignment(Qt.AlignCenter)

        self.verticalLayoutInputsNr.addWidget(self.lblInputsNr)

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


        self.verticalLayoutInputsNr.addLayout(self.formLayout)

        self.btnCalculate = QPushButton(self.tabNr)
        self.btnCalculate.setObjectName(u"btnCalculate")
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCalculate.sizePolicy().hasHeightForWidth())
        self.btnCalculate.setSizePolicy(sizePolicy)

        self.verticalLayoutInputsNr.addWidget(self.btnCalculate)

        self.vsNrButton = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayoutInputsNr.addItem(self.vsNrButton)


        self.horizontalLayout.addLayout(self.verticalLayoutInputsNr)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableResult = QTableView(self.tabNr)
        self.tableResult.setObjectName(u"tableResult")
        self.tableResult.setSortingEnabled(True)
        self.tableResult.horizontalHeader().setVisible(True)
        self.tableResult.horizontalHeader().setHighlightSections(False)

        self.verticalLayout_4.addWidget(self.tableResult)

        self.hlNrButtons = QHBoxLayout()
        self.hlNrButtons.setObjectName(u"hlNrButtons")
        self.btnDeleteSelectedNr = QPushButton(self.tabNr)
        self.btnDeleteSelectedNr.setObjectName(u"btnDeleteSelectedNr")

        self.hlNrButtons.addWidget(self.btnDeleteSelectedNr)

        self.btnClearNr = QPushButton(self.tabNr)
        self.btnClearNr.setObjectName(u"btnClearNr")

        self.hlNrButtons.addWidget(self.btnClearNr)


        self.verticalLayout_4.addLayout(self.hlNrButtons)

        self.btnToggleOverhead = QPushButton(self.tabNr)
        self.btnToggleOverhead.setObjectName(u"btnToggleOverhead")

        self.verticalLayout_4.addWidget(self.btnToggleOverhead)

        self.tableOverHead = QTableView(self.tabNr)
        self.tableOverHead.setObjectName(u"tableOverHead")
        self.tableOverHead.horizontalHeader().setHighlightSections(False)

        self.verticalLayout_4.addWidget(self.tableOverHead)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tabNr, "")
        self.tabLte = QWidget()
        self.tabLte.setObjectName(u"tabLte")
        self.horizontalLayout_3 = QHBoxLayout(self.tabLte)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lblInputsLte = QLabel(self.tabLte)
        self.lblInputsLte.setObjectName(u"lblInputsLte")
        self.lblInputsLte.setFont(font)
        self.lblInputsLte.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.lblInputsLte)

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
        self.spinResourceBlocksLte.setMaximum(110)
        self.spinResourceBlocksLte.setValue(50)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.spinResourceBlocksLte)

        self.label = QLabel(self.tabLte)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label)

        self.comboLteSlPeriod = QComboBox(self.tabLte)
        self.comboLteSlPeriod.setObjectName(u"comboLteSlPeriod")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.comboLteSlPeriod)

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

        self.vsLteButton = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.vsLteButton)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableResultLte = QTableView(self.tabLte)
        self.tableResultLte.setObjectName(u"tableResultLte")
        self.tableResultLte.setSortingEnabled(True)
        self.tableResultLte.horizontalHeader().setHighlightSections(False)

        self.verticalLayout_5.addWidget(self.tableResultLte)

        self.hlLteButtons = QHBoxLayout()
        self.hlLteButtons.setObjectName(u"hlLteButtons")
        self.btnDeleteSelectedLte = QPushButton(self.tabLte)
        self.btnDeleteSelectedLte.setObjectName(u"btnDeleteSelectedLte")

        self.hlLteButtons.addWidget(self.btnDeleteSelectedLte)

        self.btnClearLte = QPushButton(self.tabLte)
        self.btnClearLte.setObjectName(u"btnClearLte")

        self.hlLteButtons.addWidget(self.btnClearLte)


        self.verticalLayout_5.addLayout(self.hlLteButtons)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tabLte, "")
        self.tabCharts = QWidget()
        self.tabCharts.setObjectName(u"tabCharts")
        self.horizontalLayout_4 = QHBoxLayout(self.tabCharts)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayoutChart1 = QVBoxLayout()
        self.verticalLayoutChart1.setSpacing(0)
        self.verticalLayoutChart1.setObjectName(u"verticalLayoutChart1")
        self.lblChartNr = QLabel(self.tabCharts)
        self.lblChartNr.setObjectName(u"lblChartNr")
        font1 = QFont()
        font1.setPointSize(15)
        self.lblChartNr.setFont(font1)
        self.lblChartNr.setAlignment(Qt.AlignCenter)

        self.verticalLayoutChart1.addWidget(self.lblChartNr)

        self.chartNr = QtCharts.QChartView(self.tabCharts)
        self.chartNr.setObjectName(u"chartNr")

        self.verticalLayoutChart1.addWidget(self.chartNr)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.comboNrChartXAxis = QComboBox(self.tabCharts)
        self.comboNrChartXAxis.setObjectName(u"comboNrChartXAxis")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.comboNrChartXAxis)

        self.lblNrChartYAxis = QLabel(self.tabCharts)
        self.lblNrChartYAxis.setObjectName(u"lblNrChartYAxis")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.lblNrChartYAxis)

        self.comboNrChartYAxis = QComboBox(self.tabCharts)
        self.comboNrChartYAxis.setObjectName(u"comboNrChartYAxis")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.comboNrChartYAxis)

        self.lblNrChartXAxis = QLabel(self.tabCharts)
        self.lblNrChartXAxis.setObjectName(u"lblNrChartXAxis")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.lblNrChartXAxis)

        self.lblPlotSelectedNr = QLabel(self.tabCharts)
        self.lblPlotSelectedNr.setObjectName(u"lblPlotSelectedNr")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.lblPlotSelectedNr)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.hsPlotSelectedNrLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.hsPlotSelectedNrLeft)

        self.checkPlotSelectedNr = QCheckBox(self.tabCharts)
        self.checkPlotSelectedNr.setObjectName(u"checkPlotSelectedNr")
        self.checkPlotSelectedNr.setIconSize(QSize(16, 16))

        self.horizontalLayout_5.addWidget(self.checkPlotSelectedNr)

        self.hsPlotSelectedNrRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.hsPlotSelectedNrRight)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_5)


        self.verticalLayoutChart1.addLayout(self.formLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayoutChart1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lblChartLte = QLabel(self.tabCharts)
        self.lblChartLte.setObjectName(u"lblChartLte")
        self.lblChartLte.setFont(font1)
        self.lblChartLte.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.lblChartLte)

        self.chartLte = QtCharts.QChartView(self.tabCharts)
        self.chartLte.setObjectName(u"chartLte")

        self.verticalLayout_3.addWidget(self.chartLte)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.lblLteChartXAxis = QLabel(self.tabCharts)
        self.lblLteChartXAxis.setObjectName(u"lblLteChartXAxis")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.lblLteChartXAxis)

        self.comboLteChartXAxis = QComboBox(self.tabCharts)
        self.comboLteChartXAxis.setObjectName(u"comboLteChartXAxis")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.comboLteChartXAxis)

        self.lblLteChartYAxis = QLabel(self.tabCharts)
        self.lblLteChartYAxis.setObjectName(u"lblLteChartYAxis")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.lblLteChartYAxis)

        self.comboLteChartYAxis = QComboBox(self.tabCharts)
        self.comboLteChartYAxis.setObjectName(u"comboLteChartYAxis")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.comboLteChartYAxis)

        self.lblPlotSelectedLte = QLabel(self.tabCharts)
        self.lblPlotSelectedLte.setObjectName(u"lblPlotSelectedLte")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.lblPlotSelectedLte)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.hsPlotSelectedLteLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.hsPlotSelectedLteLeft)

        self.checkPlotSelectedLte = QCheckBox(self.tabCharts)
        self.checkPlotSelectedLte.setObjectName(u"checkPlotSelectedLte")

        self.horizontalLayout_6.addWidget(self.checkPlotSelectedLte)

        self.hsPlotSelectedLteRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.hsPlotSelectedLteRight)


        self.formLayout_4.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_6)


        self.verticalLayout_3.addLayout(self.formLayout_4)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tabCharts, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1422, 24))
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menuExport.addAction(self.action_CSV)
        self.menuEdit.addAction(self.actionClear_Tables)
        self.menuEdit.addAction(self.actionDelete_Selected)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"5G NR/LTE Maximum Sidelink Capacity Estimator", None))
        self.action_CSV.setText(QCoreApplication.translate("MainWindow", u"&CSV", None))
        self.actionClear_Tables.setText(QCoreApplication.translate("MainWindow", u"&Clear Tables", None))
        self.actionDelete_Selected.setText(QCoreApplication.translate("MainWindow", u"&Delete Selected", None))
        self.lblInputsNr.setText(QCoreApplication.translate("MainWindow", u"Inputs", None))
        self.lblNumerology.setText(QCoreApplication.translate("MainWindow", u"Numerology", None))
        self.lblResourceBlocks.setText(QCoreApplication.translate("MainWindow", u"# PRBs", None))
        self.spinResourceBlocksNr.setSuffix("")
        self.lblLayers.setText(QCoreApplication.translate("MainWindow", u"# Layers", None))
#if QT_CONFIG(tooltip)
        self.lblModulation.setToolTip(QCoreApplication.translate("MainWindow", u"Max modulation supported by the UE", None))
#endif // QT_CONFIG(tooltip)
        self.lblModulation.setText(QCoreApplication.translate("MainWindow", u"Max Modulation", None))
        self.lblHarq.setText(QCoreApplication.translate("MainWindow", u"HARQ Mode", None))
        self.lblBlindTransmissions.setText(QCoreApplication.translate("MainWindow", u"Blind Transmissions", None))
        self.lblFeedbackChannel.setText(QCoreApplication.translate("MainWindow", u"Feedback Channel Period (slot)", None))
        self.btnCalculate.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
        self.btnDeleteSelectedNr.setText(QCoreApplication.translate("MainWindow", u"Delete Selected", None))
        self.btnClearNr.setText(QCoreApplication.translate("MainWindow", u"Clear Table", None))
        self.btnToggleOverhead.setText(QCoreApplication.translate("MainWindow", u"Hide Overhead Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNr), QCoreApplication.translate("MainWindow", u"NR", None))
        self.lblInputsLte.setText(QCoreApplication.translate("MainWindow", u"Inputs", None))
        self.lblMcs.setText(QCoreApplication.translate("MainWindow", u"MCS", None))
        self.lblResourceBlocks_2.setText(QCoreApplication.translate("MainWindow", u"Resource Blocks", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sidelink Period", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PSCCH Length", None))
        self.spinPscchSize.setSuffix(QCoreApplication.translate("MainWindow", u" Subframes", None))
        self.btnCalculateLte.setText(QCoreApplication.translate("MainWindow", u"Calculate Data Rate", None))
        self.btnDeleteSelectedLte.setText(QCoreApplication.translate("MainWindow", u"Delete Selected", None))
        self.btnClearLte.setText(QCoreApplication.translate("MainWindow", u"Clear Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLte), QCoreApplication.translate("MainWindow", u"LTE", None))
        self.lblChartNr.setText(QCoreApplication.translate("MainWindow", u"NR", None))
        self.lblNrChartYAxis.setText(QCoreApplication.translate("MainWindow", u"Y Axis", None))
        self.lblNrChartXAxis.setText(QCoreApplication.translate("MainWindow", u"X Axis", None))
        self.lblPlotSelectedNr.setText(QCoreApplication.translate("MainWindow", u"Plot Selected Only", None))
        self.checkPlotSelectedNr.setText("")
        self.lblChartLte.setText(QCoreApplication.translate("MainWindow", u"LTE", None))
        self.lblLteChartXAxis.setText(QCoreApplication.translate("MainWindow", u"X Axis", None))
        self.lblLteChartYAxis.setText(QCoreApplication.translate("MainWindow", u"Y Axis", None))
        self.lblPlotSelectedLte.setText(QCoreApplication.translate("MainWindow", u"Plot Selected Only", None))
        self.checkPlotSelectedLte.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCharts), QCoreApplication.translate("MainWindow", u"Charts", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"E&xport", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
    # retranslateUi

