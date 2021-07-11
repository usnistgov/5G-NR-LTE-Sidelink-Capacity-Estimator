# NIST-developed software is provided by NIST as a public service. You may use,
# copy and distribute copies of the software in any medium, provided that you
# keep intact this entire notice. You may improve,modify and create derivative
# works of the software or any portion of the software, and you may copy and
# distribute such modifications or works. Modified works should carry a notice
# stating that you changed the software and should note the date and nature of
# any such change. Please explicitly acknowledge the National Institute of
# Standards and Technology as the source of the software.
#
# NIST-developed software is expressly provided "AS IS." NIST MAKES NO
# WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT OR ARISING BY OPERATION OF
# LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT
# AND DATA ACCURACY. NIST NEITHER REPRESENTS NOR WARRANTS THAT THE
# OPERATION OF THE SOFTWARE WILL BE UNINTERRUPTED OR ERROR-FREE, OR THAT
# ANY DEFECTS WILL BE CORRECTED. NIST DOES NOT WARRANT OR MAKE ANY
# REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR THE RESULTS THEREOF,
# INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY, RELIABILITY,
# OR USEFULNESS OF THE SOFTWARE.
#
# You are solely responsible for determining the appropriateness of using and
# distributing the software and you assume all risks associated with its use,
# including but not limited to the risks and costs of program errors,
# compliance with applicable laws, damage to or loss of data, programs or
# equipment, and the unavailability or interruption of operation. This
# software is not intended to be used in any situation where a failure could
# cause risk of injury or damage to property. The software developed by NIST
# employees is not subject to copyright protection within the United States.

from core import calculate_nr, HarqMode, OutOfRangeError
from typing import List, Union, Any, Optional
import PySide2.QtCore as QtCore
from PySide2.QtCore import Qt, QMargins, QAbstractTableModel, QModelIndex
from PySide2.QtCharts import QtCharts
from PySide2.QtWidgets import QMainWindow, QHeaderView, QMessageBox
from ui_mainwindow import Ui_MainWindow


class ResultRow:
    def __init__(self, run: int, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
                 harq_mode: HarqMode, result: float, blind_retransmissions: Optional[int],
                 feedback_channel_period: Optional[int]):
        self.run = run
        self.numerology = numerology
        self.resource_blocks = resource_blocks
        self.layers = layers
        self.max_modulation = max_modulation
        self.harq_mode = harq_mode
        self.result = result
        self.blind_retransmissions = blind_retransmissions
        self.feedback_channel_period = feedback_channel_period


class ResultTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRow] = []

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 9

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:

        if role == Qt.DisplayRole:
            result = self._results[index.row()]
            if index.column() == 0:
                return result.run
            elif index.column() == 1:
                return result.numerology
            elif index.column() == 2:
                return result.resource_blocks
            elif index.column() == 3:
                return result.layers
            elif index.column() == 4:
                return result.max_modulation
            elif index.column() == 5:
                if result.harq_mode == HarqMode.BLIND_TRANSMISSION:
                    return "Blind Transmission"
                elif result.harq_mode == HarqMode.FEEDBACK:
                    return "Feedback"
                else:
                    raise ValueError("Unsupported HARQ Mode")
            elif index.column() == 6:
                if result.harq_mode == HarqMode.BLIND_TRANSMISSION:
                    return result.blind_retransmissions
                else:
                    return "N/A"
            elif index.column() == 7:
                if result.harq_mode == HarqMode.FEEDBACK:
                    return result.feedback_channel_period
                else:
                    return "N/A"
            elif index.column() == 8:
                return result.result

        if role == Qt.TextAlignmentRole:
            if index.column() != 5:
                return Qt.AlignRight  # TODO: AlignVCenter as well

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section == 0:
            return "Run Index"
        elif section == 1:
            return "Numerology"
        elif section == 2:
            return "Resource Blocks (PRB)"
        elif section == 3:
            return "Layers"
        elif section == 4:
            return "Max Modulation (QAM)"
        elif section == 5:
            return "HARQ Mode"
        elif section == 6:
            return "Blind Transmissions"
        elif section == 7:
            return "Feedback Channel Period"
        elif section == 8:
            return "Data Rate (Mbps)"

    def append(self, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
               harq_mode: HarqMode, result: float, blind_retransmissions: Optional[int],
               feedback_channel_period: Optional[int]):
        new_result = ResultRow(
            run=len(self._results),
            numerology=numerology,
            resource_blocks=resource_blocks,
            layers=layers,
            max_modulation=max_modulation,
            harq_mode=harq_mode,
            result=result,
            blind_retransmissions=blind_retransmissions,
            feedback_channel_period=feedback_channel_period
        )

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.comboNumerology.addItem("0", userData=0)
        self.ui.comboNumerology.addItem("1", userData=1)

        self.ui.comboLayers.addItem("1", userData=1)
        self.ui.comboLayers.addItem("2", userData=2)
        # Have 2 Layers selected by default
        self.ui.comboLayers.setCurrentIndex(self.ui.comboLayers.findData(2, Qt.UserRole))

        self.ui.comboModulation.addItem("64 QAM", userData=64)
        self.ui.comboModulation.addItem("256 QAM", userData=256)

        self.ui.comboHarq.addItem("Blind Transmission", userData=HarqMode.BLIND_TRANSMISSION)
        self.ui.comboHarq.addItem("Feedback Channel", userData=HarqMode.FEEDBACK)

        # Manually trigger this slot, so we only see the relevant inputs for the starting HARQ mode
        self.harq_mode_changed()

        self.ui.comboFeedbackChannel.addItem("1", userData=1)
        self.ui.comboFeedbackChannel.addItem("2", userData=2)
        self.ui.comboFeedbackChannel.addItem("4", userData=4)

        # Charts
        self.chart = QtCharts.QChart()
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.legend().setVisible(False)

        self.series = QtCharts.QBarSeries()
        bar_set = QtCharts.QBarSet("Result")
        self.series.append(bar_set)
        self.chart.addSeries(self.series)

        self.x_axis = QtCharts.QBarCategoryAxis()
        self.x_axis.append(["SCS 15kHz"])
        self.chart.addAxis(self.x_axis, Qt.AlignBottom)
        self.series.attachAxis(self.x_axis)

        self.y_axis = QtCharts.QValueAxis()
        self.y_axis.setRange(0, 100)
        self.y_axis.setTickCount(12)
        # self.y_axis.setTickInterval(10)
        self.y_axis.applyNiceNumbers()

        self.y_axis.setTitleText("Mbps")
        self.chart.addAxis(self.y_axis, Qt.AlignLeft)
        self.series.attachAxis(self.y_axis)

        self.ui.chartView.setChart(self.chart)
        self.ui.chartView.setVisible(False)

        # Result table

        self.tableModel = ResultTableModel()
        self.ui.tableResult.setModel(self.tableModel)
        self.ui.tableResult.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResult.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # Signals
        self.ui.btnCalculate.clicked.connect(self.btn_clicked)
        self.ui.comboNumerology.activated.connect(self.numerology_changed)
        self.ui.comboHarq.activated.connect(self.harq_mode_changed)

    @QtCore.Slot()
    def numerology_changed(self):  # We don't need the new index, so ignore it
        numerology = int(self.ui.comboNumerology.currentData(Qt.UserRole))
        if numerology == 0:
            self.ui.spinResourceBlocks.setMaximum(52)
            self.ui.spinResourceBlocks.setValue(52)
        elif numerology == 1:
            self.ui.spinResourceBlocks.setMaximum(24)
            self.ui.spinResourceBlocks.setValue(24)
        else:
            raise ValueError("Unsupported Numerology")

    @QtCore.Slot()
    def harq_mode_changed(self):  # We don't need the new index, so ignore it
        harq_mode = self.ui.comboHarq.currentData(Qt.UserRole)
        if harq_mode == HarqMode.BLIND_TRANSMISSION:
            self.ui.lblFeedbackChannel.hide()
            self.ui.comboFeedbackChannel.hide()

            self.ui.lblBlindTransmissions.show()
            self.ui.spinBlindTransmissions.show()
        elif harq_mode == HarqMode.FEEDBACK:
            self.ui.lblBlindTransmissions.hide()
            self.ui.spinBlindTransmissions.hide()

            self.ui.lblFeedbackChannel.show()
            self.ui.comboFeedbackChannel.show()
        else:
            raise ValueError("Unsupported HARQ mode")

    @QtCore.Slot()
    def btn_clicked(self):
        numerology = int(self.ui.comboNumerology.currentData(Qt.UserRole))
        resource_blocks = self.ui.spinResourceBlocks.value()
        layers = int(self.ui.comboLayers.currentData(Qt.UserRole))
        max_modulation = int(self.ui.comboModulation.currentData(Qt.UserRole))
        harq_mode = self.ui.comboHarq.currentData(Qt.UserRole)

        blind_retransmissions = None
        if harq_mode == HarqMode.BLIND_TRANSMISSION:
            blind_retransmissions = self.ui.spinBlindTransmissions.value()

        feedback_channel_period = None
        if harq_mode == HarqMode.FEEDBACK:
            feedback_channel_period = self.ui.comboFeedbackChannel.currentData(Qt.UserRole)

        try:
            data_rate = calculate_nr(numerology=numerology, resource_blocks=resource_blocks, layers=layers,
                                     ue_max_modulation=max_modulation,
                                     harq_mode=harq_mode, blind_transmissions=blind_retransmissions,
                                     feedback_channel_period=feedback_channel_period)
        except OutOfRangeError as e:
            QMessageBox.critical(self, "Value out of Range", str(e))
            return
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Value", str(e))
            return

        self.tableModel.append(
            numerology=numerology,
            resource_blocks=resource_blocks,
            layers=layers,
            max_modulation=max_modulation,
            harq_mode=harq_mode,
            result=data_rate,
            blind_retransmissions=blind_retransmissions,
            feedback_channel_period=feedback_channel_period,
        )
        self.series.barSets()[0].insert(0, data_rate)
