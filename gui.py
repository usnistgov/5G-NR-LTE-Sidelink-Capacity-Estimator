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
import csv

from core import calculate_nr, NrResult, calculate_lte, HarqMode, OutOfRangeError
from typing import List, Union, Any, Optional
import PySide2.QtCore as QtCore
from PySide2.QtCore import Qt, QMargins, QAbstractTableModel, QModelIndex
from PySide2.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QDialog, QAbstractButton, QFileDialog
from PySide2.QtCharts import *
from ui_mainwindow import Ui_MainWindow
from ui_csvdialog import Ui_CsvDialog
from enum import Enum


class ExportTable(Enum):
    NR = 0
    LTE = 1


class CsvDialog(QDialog):
    def __init__(self, parent=None):
        super(CsvDialog, self).__init__(parent)
        self.ui = Ui_CsvDialog()
        self.ui.setupUi(self)

        self.ui.comboTable.addItem("NR", userData=ExportTable.NR.value)
        self.ui.comboTable.addItem("LTE", userData=ExportTable.LTE.value)

        # Have one selected by default
        self.ui.comboTable.setCurrentIndex(self.ui.comboTable.findData(ExportTable.NR.value, Qt.UserRole))

    def selected_table(self) -> ExportTable:
        data = self.ui.comboTable.currentData(Qt.UserRole)
        if data == ExportTable.NR.value:
            return ExportTable.NR
        else:
            return ExportTable.LTE


class NrTableColumn(Enum):
    RUN_INDEX = 0
    NUMEROLOGY = 1
    RESOURCE_BLOCKS = 2
    LAYERS = 3
    UE_MAX_MODULATION = 4
    HARQ_MODE = 5
    BLIND_TRANSMISSIONS = 6
    FEEDBACK_CHANNEL_PERIOD = 7
    DATA_RATE = 8

    def __str__(self):
        if self is NrTableColumn.RUN_INDEX:
            return "Run Index"
        elif self is NrTableColumn.NUMEROLOGY:
            return "Numerology"
        elif self is NrTableColumn.RESOURCE_BLOCKS:
            return "Resource Blocks"
        elif self is NrTableColumn.LAYERS:
            return "Layers"
        elif self is NrTableColumn.UE_MAX_MODULATION:
            return "UE Max Modulation"
        elif self is NrTableColumn.HARQ_MODE:
            return "HARQ Mode"
        elif self is NrTableColumn.BLIND_TRANSMISSIONS:
            return "Blind Transmissions"
        elif self is NrTableColumn.FEEDBACK_CHANNEL_PERIOD:
            return "Feedback Channel Period"
        elif self is NrTableColumn.DATA_RATE:
            return "Data Rate (Mbps)"


class ResultRow:
    def __init__(self, run: int, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
                 harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
                 feedback_channel_period: Optional[int]):
        self.run = run
        self.numerology = numerology
        self.resource_blocks = resource_blocks
        self.layers = layers
        self.max_modulation = max_modulation
        self.harq_mode = harq_mode
        self.nr_result = nr_result
        self.blind_retransmissions = blind_retransmissions
        self.feedback_channel_period = feedback_channel_period

    def to_csv(self):
        return [self.run, self.numerology, self.resource_blocks, self.layers, self.max_modulation, str(self.harq_mode),
                self.blind_retransmissions, self.feedback_channel_period, self.nr_result.data_rate]


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
                return result.nr_result.data_rate

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
            return "UE Max Modulation (QAM)"
        elif section == 5:
            return "HARQ Mode"
        elif section == 6:
            return "Blind Transmissions"
        elif section == 7:
            return "Feedback Channel Period"
        elif section == 8:
            return "Data Rate (Mbps)"

    def append(self, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
               harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
               feedback_channel_period: Optional[int]):
        new_result = ResultRow(
            run=len(self._results),
            numerology=numerology,
            resource_blocks=resource_blocks,
            layers=layers,
            max_modulation=max_modulation,
            harq_mode=harq_mode,
            nr_result=nr_result,
            blind_retransmissions=blind_retransmissions,
            feedback_channel_period=feedback_channel_period
        )

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()

    def results(self):
        return self._results

    def get_result(self, row: int) -> ResultRow:
        return self._results[row]


class OverheadTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._currentResult: Optional[NrResult] = None

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 10

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 2

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight  # TODO: AlignVCenter as well

        if role == Qt.DisplayRole and self._currentResult is not None:
            if index.column() == 0:
                if index.row() == 0:
                    return self._currentResult.psfch
                elif index.row() == 1:
                    return self._currentResult.csi_rs
                elif index.row() == 2:
                    return self._currentResult.pt_rs
                elif index.row() == 3:
                    return self._currentResult.pscch
                elif index.row() == 4:
                    return self._currentResult.sci2
                elif index.row() == 5:
                    return self._currentResult.dm_rs
                elif index.row() == 6:
                    return self._currentResult.agc
                elif index.row() == 7:
                    return self._currentResult.guard
                elif index.row() == 8:
                    return self._currentResult.s_ssb
                elif index.row() == 9:
                    return self._currentResult.overhead_total
            elif index.column() == 1:
                if index.row() == 0:
                    return self._currentResult.psfch / self._currentResult.overhead_total * 100
                elif index.row() == 1:
                    return self._currentResult.csi_rs / self._currentResult.overhead_total * 100
                elif index.row() == 2:
                    return self._currentResult.pt_rs / self._currentResult.overhead_total * 100
                elif index.row() == 3:
                    return self._currentResult.pscch / self._currentResult.overhead_total * 100
                elif index.row() == 4:
                    return self._currentResult.sci2 / self._currentResult.overhead_total * 100
                elif index.row() == 5:
                    return self._currentResult.dm_rs / self._currentResult.overhead_total * 100
                elif index.row() == 6:
                    return self._currentResult.agc / self._currentResult.overhead_total * 100
                elif index.row() == 7:
                    return self._currentResult.guard / self._currentResult.overhead_total * 100
                elif index.row() == 8:
                    return self._currentResult.s_ssb / self._currentResult.overhead_total * 100
                elif index.row() == 9:
                    return 100.00

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role != Qt.DisplayRole:
            return

        if orientation == Qt.Vertical:
            if section == 0:
                return "PSFCH"
            elif section == 1:
                return "CSI-RS"
            elif section == 2:
                return "PT-RS"
            elif section == 3:
                return "PSCCH"
            elif section == 4:
                return "SCI2"
            elif section == 5:
                return "DM-RS"
            elif section == 6:
                return "AGC"
            elif section == 7:
                return "Guard"
            elif section == 8:
                return "S-SSB"
            elif section == 9:
                return "Total"

        # TODO: Horizontal Headers
        if orientation == Qt.Horizontal:
            if section == 0:
                return "Overhead Components"
            elif section == 1:
                return "Percent Total Overhead"

    def set_result(self, nr_result: NrResult):
        self._currentResult = nr_result
        self.dataChanged.emit(QModelIndex(), QModelIndex())


class LteTableColumn(Enum):
    RUN_INDEX = 0
    MCS = 1
    RESOURCE_BLOCKS = 2
    PERIOD_SIZE = 3
    PSCCH_SIZE = 4
    DATA_RATE = 5

    def __str__(self):
        if self is LteTableColumn.RUN_INDEX:
            return "Run Index"
        elif self is LteTableColumn.MCS:
            return "MCS"
        elif self is LteTableColumn.RESOURCE_BLOCKS:
            return "Resource Blocks (PRB)"
        elif self is LteTableColumn.PERIOD_SIZE:
            return "Period Size [SF]"
        elif self is LteTableColumn.PSCCH_SIZE:
            return "PSCCH Size [SF]"
        elif self is LteTableColumn.DATA_RATE:
            return "Data Rate (Mbps)"


class ResultRowLte:
    def __init__(self, run: int, mcs: int, resource_blocks: int, period_size: int, pscch_size: int, result: float):
        self.run = run
        self.mcs = mcs
        self.resource_blocks = resource_blocks
        self.period_size = period_size
        self.pscch_size = pscch_size
        self.result = result

    def to_csv(self):
        return [self.run, self.mcs, self.resource_blocks, self.period_size, self.pscch_size, self.result]


class ResultTableLteModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRowLte] = []

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 6

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:

        if role == Qt.DisplayRole:
            result = self._results[index.row()]
            if index.column() == 0:
                return result.run
            elif index.column() == 1:
                return result.mcs
            elif index.column() == 2:
                return result.resource_blocks
            elif index.column() == 3:
                return result.period_size
            elif index.column() == 4:
                return result.pscch_size
            elif index.column() == 5:
                return result.result

        if role == Qt.TextAlignmentRole:
            return Qt.AlignRight  # TODO: AlignVCenter as well

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section == 0:
            return "Run Index"
        elif section == 1:
            return "MCS"
        elif section == 2:
            return "Resource Blocks (PRB)"
        elif section == 3:
            return "Period Size [SF]"
        elif section == 4:
            return "PSCCH Size [SF]"
        elif section == 5:
            return "Data Rate (Mbps)"

    def append(self, mcs: int, resource_blocks: int, period_size: int, pscch_size: int, result: float):
        new_result = ResultRowLte(
            run=len(self._results),
            mcs=mcs,
            resource_blocks=resource_blocks,
            period_size=period_size,
            pscch_size=pscch_size,
            result=result
        )

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()

    def results(self):
        return self._results


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

        # Remove margins around charts
        self.ui.chartNr.chart().layout().setContentsMargins(0, 0, 0, 0)
        self.ui.chartLte.chart().layout().setContentsMargins(0, 0, 0, 0)

        for table_item in list(NrTableColumn):
            self.ui.comboNrChartXAxis.addItem(str(table_item), userData=table_item.value)
            self.ui.comboNrChartYAxis.addItem(str(table_item), userData=table_item.value)

        for table_item in list(LteTableColumn):
            self.ui.comboLteChartXAxis.addItem(str(table_item), userData=table_item.value)
            self.ui.comboLteChartYAxis.addItem(str(table_item), userData=table_item.value)

        # Result table

        self.tableModel = ResultTableModel()
        self.ui.tableResult.setModel(self.tableModel)
        self.ui.tableResult.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResult.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # NR Overhead Table

        self.tableModelOverHead = OverheadTableModel()
        self.ui.tableOverHead.setModel(self.tableModelOverHead)
        self.ui.tableOverHead.horizontalHeader().setStretchLastSection(True)
        self.ui.tableOverHead.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # LTE Result Table

        self.tableModelLte = ResultTableLteModel()
        self.ui.tableResultLte.setModel(self.tableModelLte)
        self.ui.tableResultLte.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResultLte.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # Signals
        self.ui.btnCalculate.clicked.connect(self.btn_clicked)
        self.ui.btnToggleOverhead.clicked.connect(self.toggle_overhead_table_clicked)
        self.ui.tableResult.clicked.connect(self.row_clicked_nr)
        self.ui.comboNumerology.activated.connect(self.numerology_changed)
        self.ui.comboHarq.activated.connect(self.harq_mode_changed)
        self.ui.btnCalculateLte.clicked.connect(self.btn_clicked_lte)

        self.ui.comboNrChartXAxis.activated.connect(self.chart_nr_axis_changed)
        self.ui.comboNrChartYAxis.activated.connect(self.chart_nr_axis_changed)

        self.ui.comboLteChartXAxis.activated.connect(self.chart_lte_axis_changed)
        self.ui.comboLteChartYAxis.activated.connect(self.chart_lte_axis_changed)

        self.ui.action_CSV.triggered.connect(self.export_csv)

    @QtCore.Slot()
    def export_csv(self):
        dialog = CsvDialog(self)
        if not dialog.exec_():
            return
        file = QFileDialog.getSaveFileName(self, caption="Save CSV", dir="export.csv", filter="CSV (*.csv)")
        # No file selected
        if not file[0]:
            return
        with open(file[0], mode='w') as csv_file:
            selected_table = dialog.selected_table()
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')

            results = []
            if selected_table == ExportTable.NR:
                if dialog.ui.checkHeaders.isChecked():
                    writer.writerow(list(NrTableColumn))
                results = self.tableModel.results()
            else:
                if dialog.ui.checkHeaders.isChecked():
                    writer.writerow(list(LteTableColumn))
                results = self.tableModelLte.results()

            for result in results:
                writer.writerow(result.to_csv())

    @QtCore.Slot()
    def numerology_changed(self):  # We don't need the new index, so ignore it
        numerology = int(self.ui.comboNumerology.currentData(Qt.UserRole))
        if numerology == 0:
            self.ui.spinResourceBlocksNr.setMaximum(52)
            self.ui.spinResourceBlocksNr.setValue(52)
        elif numerology == 1:
            self.ui.spinResourceBlocksNr.setMaximum(24)
            self.ui.spinResourceBlocksNr.setValue(24)
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
        resource_blocks = self.ui.spinResourceBlocksNr.value()
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
            nr_result = calculate_nr(numerology=numerology, resource_blocks=resource_blocks, layers=layers,
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
            nr_result=nr_result,
            blind_retransmissions=blind_retransmissions,
            feedback_channel_period=feedback_channel_period,
        )
        # Update the chart with the new result
        self.chart_nr_axis_changed()

    def value_for_axis(self, result: ResultRow, column: NrTableColumn):
        if column == NrTableColumn.RUN_INDEX:
            return result.run
        elif column == NrTableColumn.NUMEROLOGY:
            return result.numerology
        elif column == NrTableColumn.RESOURCE_BLOCKS:
            return result.resource_blocks
        elif column == NrTableColumn.LAYERS:
            return result.layers
        elif column == NrTableColumn.UE_MAX_MODULATION:
            return result.max_modulation
        elif column == NrTableColumn.HARQ_MODE:
            return result.harq_mode.value
        elif column == NrTableColumn.BLIND_TRANSMISSIONS:
            if result.blind_retransmissions is None:
                return 0
            return result.blind_retransmissions
        elif column == NrTableColumn.FEEDBACK_CHANNEL_PERIOD:
            if result.feedback_channel_period is None:
                return 0
            return result.feedback_channel_period
        elif column == NrTableColumn.DATA_RATE:
            return result.nr_result.data_rate

    def value_for_axis_lte(self, result: ResultRowLte, column: LteTableColumn):
        if column == LteTableColumn.RUN_INDEX:
            return result.run
        elif column == LteTableColumn.MCS:
            return result.mcs
        elif column == LteTableColumn.RESOURCE_BLOCKS:
            return result.resource_blocks
        elif column == LteTableColumn.PERIOD_SIZE:
            return result.period_size
        elif column == LteTableColumn.PSCCH_SIZE:
            return result.pscch_size
        elif column == LteTableColumn.DATA_RATE:
            return result.result

    def make_harq_axis(self):
        category_axis = QtCharts.QCategoryAxis(self)
        category_axis.append(str(HarqMode.BLIND_TRANSMISSION), HarqMode.BLIND_TRANSMISSION.value)
        category_axis.append(str(HarqMode.FEEDBACK), HarqMode.FEEDBACK.value)
        category_axis.setMin(-0.01)
        category_axis.setMax(1.01)
        return category_axis

    @QtCore.Slot()
    def chart_nr_axis_changed(self):
        x_value = NrTableColumn(self.ui.comboNrChartXAxis.currentData(Qt.UserRole))
        y_value = NrTableColumn(self.ui.comboNrChartYAxis.currentData(Qt.UserRole))

        series = QtCharts.QLineSeries()

        for result in self.tableModel.results():
            series.append(self.value_for_axis(result, x_value), self.value_for_axis(result, y_value))

        chart = QtCharts.QChart()
        chart.setTitle(f"NR: '{x_value}' - '{y_value}'")
        chart.addSeries(series)
        chart.createDefaultAxes()

        # Special Handling for HARQ Mode, since those are Enum values
        if x_value == NrTableColumn.HARQ_MODE:
            chart.setAxisX(self.make_harq_axis(), series)
        if y_value == NrTableColumn.HARQ_MODE:
            chart.setAxisY(self.make_harq_axis(), series)

        chart.axisX().setTitleText(str(x_value))
        chart.axisY().setTitleText(str(y_value))

        self.ui.chartNr.setChart(chart)

    @QtCore.Slot()
    def chart_lte_axis_changed(self):
        x_value = LteTableColumn(self.ui.comboLteChartXAxis.currentData(Qt.UserRole))
        y_value = LteTableColumn(self.ui.comboLteChartYAxis.currentData(Qt.UserRole))

        series = QtCharts.QLineSeries()

        for result in self.tableModelLte.results():
            series.append(self.value_for_axis_lte(result, x_value), self.value_for_axis_lte(result, y_value))

        chart = QtCharts.QChart()
        chart.setTitle(f"LTE: '{x_value}' - '{y_value}'")
        chart.addSeries(series)
        chart.createDefaultAxes()
        chart.axisX().setTitleText(str(x_value))
        chart.axisY().setTitleText(str(y_value))

        self.ui.chartLte.setChart(chart)

    @QtCore.Slot()
    def btn_clicked_lte(self):
        mcs = self.ui.spinMcs.value()
        resource_blocks = self.ui.spinResourceBlocksLte.value()
        period_size = self.ui.spinPeriodSize.value()
        pscch_size = self.ui.spinPscchSize.value()

        data_rate = calculate_lte(
            mcs=mcs,
            resource_blocks=resource_blocks,
            period_size=period_size,
            control_channel_size=pscch_size
        )

        self.tableModelLte.append(
            mcs=mcs,
            resource_blocks=resource_blocks,
            period_size=period_size,
            pscch_size=pscch_size,
            result=data_rate
        )
        self.chart_lte_axis_changed()

    @QtCore.Slot()
    def toggle_overhead_table_clicked(self):
        self.ui.tableOverHead.setVisible(not self.ui.tableOverHead.isVisible())
        if self.ui.tableOverHead.isVisible():
            self.ui.btnToggleOverhead.setText("⮟ Toggle Overhead")
        else:
            self.ui.btnToggleOverhead.setText("⮞ Toggle Overhead")

    @QtCore.Slot()
    def row_clicked_nr(self, index: QModelIndex):
        result = self.tableModel.get_result(index.row())
        self.tableModelOverHead.set_result(result.nr_result)
