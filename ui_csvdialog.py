# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'csv_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CsvDialog(object):
    def setupUi(self, CsvDialog):
        if not CsvDialog.objectName():
            CsvDialog.setObjectName(u"CsvDialog")
        CsvDialog.setWindowModality(Qt.ApplicationModal)
        CsvDialog.resize(415, 152)
        CsvDialog.setStyleSheet(u"QCheckBox::indicator {\n"
"     width: 20px;\n"
"     height: 20px;\n"
"}")
        self.formLayout = QFormLayout(CsvDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.lblTable = QLabel(CsvDialog)
        self.lblTable.setObjectName(u"lblTable")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblTable)

        self.comboTable = QComboBox(CsvDialog)
        self.comboTable.setObjectName(u"comboTable")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboTable)

        self.buttons = QDialogButtonBox(CsvDialog)
        self.buttons.setObjectName(u"buttons")
        self.buttons.setOrientation(Qt.Horizontal)
        self.buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.buttons)

        self.hlHeader = QHBoxLayout()
        self.hlHeader.setObjectName(u"hlHeader")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlHeader.addItem(self.horizontalSpacer)

        self.checkOverhead = QCheckBox(CsvDialog)
        self.checkOverhead.setObjectName(u"checkOverhead")
        self.checkOverhead.setChecked(True)

        self.hlHeader.addWidget(self.checkOverhead)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlHeader.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.hlHeader)

        self.hlOverhead = QHBoxLayout()
        self.hlOverhead.setObjectName(u"hlOverhead")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlOverhead.addItem(self.horizontalSpacer_3)

        self.checkHeaders = QCheckBox(CsvDialog)
        self.checkHeaders.setObjectName(u"checkHeaders")
        self.checkHeaders.setChecked(True)

        self.hlOverhead.addWidget(self.checkHeaders)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hlOverhead.addItem(self.horizontalSpacer_4)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.hlOverhead)

        self.lblHeader = QLabel(CsvDialog)
        self.lblHeader.setObjectName(u"lblHeader")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblHeader)

        self.lblOverhead = QLabel(CsvDialog)
        self.lblOverhead.setObjectName(u"lblOverhead")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblOverhead)


        self.retranslateUi(CsvDialog)
        self.buttons.accepted.connect(CsvDialog.accept)
        self.buttons.rejected.connect(CsvDialog.reject)

        QMetaObject.connectSlotsByName(CsvDialog)
    # setupUi

    def retranslateUi(self, CsvDialog):
        CsvDialog.setWindowTitle(QCoreApplication.translate("CsvDialog", u"Export CSV", None))
        self.lblTable.setText(QCoreApplication.translate("CsvDialog", u"Table", None))
        self.checkOverhead.setText("")
        self.checkHeaders.setText("")
        self.lblHeader.setText(QCoreApplication.translate("CsvDialog", u"Include Header Row", None))
        self.lblOverhead.setText(QCoreApplication.translate("CsvDialog", u"Include Overhead Values", None))
    # retranslateUi

