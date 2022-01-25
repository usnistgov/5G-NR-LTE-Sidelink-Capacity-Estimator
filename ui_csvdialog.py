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
        CsvDialog.resize(395, 139)
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

        self.lblHeader = QLabel(CsvDialog)
        self.lblHeader.setObjectName(u"lblHeader")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblHeader)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.checkHeaders = QCheckBox(CsvDialog)
        self.checkHeaders.setObjectName(u"checkHeaders")
        self.checkHeaders.setChecked(True)

        self.horizontalLayout.addWidget(self.checkHeaders)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)

        self.buttons = QDialogButtonBox(CsvDialog)
        self.buttons.setObjectName(u"buttons")
        self.buttons.setOrientation(Qt.Horizontal)
        self.buttons.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.buttons)


        self.retranslateUi(CsvDialog)
        self.buttons.accepted.connect(CsvDialog.accept)
        self.buttons.rejected.connect(CsvDialog.reject)

        QMetaObject.connectSlotsByName(CsvDialog)
    # setupUi

    def retranslateUi(self, CsvDialog):
        CsvDialog.setWindowTitle(QCoreApplication.translate("CsvDialog", u"Export CSV", None))
        self.lblTable.setText(QCoreApplication.translate("CsvDialog", u"Table", None))
        self.lblHeader.setText(QCoreApplication.translate("CsvDialog", u"Include Header Row", None))
        self.checkHeaders.setText("")
    # retranslateUi

