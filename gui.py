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
import PySide2

from core import calculate_nr, NrResult, calculate_lte, HarqMode, OutOfRangeError, NotAcceptableValueError, \
    POSSIBLE_SL_PERIOD_SIZES_LTE
import csv
from typing import List, Union, Any, Optional, Callable
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
from PySide2.QtCore import Qt, QObject, QMargins, QAbstractTableModel, QModelIndex
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QDialog, QAbstractButton, QFileDialog
from PySide2.QtCharts import *
from ui_mainwindow import Ui_MainWindow
from ui_csvdialog import Ui_CsvDialog
from enum import Enum
from operator import attrgetter


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

        self.ui.comboTable.currentIndexChanged.connect(self.table_changed)

    def table_changed(self):
        # Only enable the Overhead checkbox for the NR table
        self.ui.checkOverhead.setEnabled(self.ui.comboTable.currentData(Qt.UserRole) == ExportTable.NR.value)

    def selected_table(self) -> ExportTable:
        data = self.ui.comboTable.currentData(Qt.UserRole)
        if data == ExportTable.NR.value:
            return ExportTable.NR
        else:
            return ExportTable.LTE


class NrTableColumn(Enum):
    ROW_NUMBER = 0
    RUN_INDEX = 1
    NUMEROLOGY = 2
    RESOURCE_BLOCKS = 3
    LAYERS = 4
    UE_MAX_MODULATION = 5
    HARQ_MODE = 6
    BLIND_TRANSMISSIONS = 7
    FEEDBACK_CHANNEL_PERIOD = 8
    DATA_RATE = 9

    def __str__(self):
        if self is NrTableColumn.ROW_NUMBER:
            return "Row"
        elif self is NrTableColumn.RUN_INDEX:
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
            return "# Blind Transmissions"
        elif self is NrTableColumn.FEEDBACK_CHANNEL_PERIOD:
            return "Feedback Channel Period"
        elif self is NrTableColumn.DATA_RATE:
            return "Data Rate (Mb/s)"


class ResultRow:
    def __init__(self, row: int, run: int, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
                 harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
                 feedback_channel_period: Optional[int]):
        self.row = row
        self.run = run
        self.numerology = numerology
        self.resource_blocks = resource_blocks
        self.layers = layers
        self.max_modulation = max_modulation
        self.harq_mode = harq_mode
        self.nr_result = nr_result
        self.blind_retransmissions = blind_retransmissions
        self.feedback_channel_period = feedback_channel_period

    # Match the `NrTableColumn` enum order
    def to_csv(self):
        return [self.row, self.run, self.numerology, self.resource_blocks, self.layers,
                str(self.max_modulation) + "QAM", str(self.harq_mode), self.blind_retransmissions,
                self.feedback_channel_period, self.nr_result.data_rate]

    def _overhead_row(self, value: float):
        return [value, value / self.nr_result.overhead_total * 100, value / self.nr_result.resource_total * 100]

    def to_csv_overhead(self):
        result = self.nr_result
        data = self.to_csv()
        # PSFCH
        data.extend(self._overhead_row(result.psfch))
        # CSI-RS
        data.extend(self._overhead_row(result.csi_rs))
        # PT-RS
        data.extend(self._overhead_row(result.pt_rs))
        # PSCCH
        data.extend(self._overhead_row(result.pscch))
        # SCI2
        data.extend(self._overhead_row(result.sci2))
        # DM-RS
        data.extend(self._overhead_row(result.dm_rs))
        # AGC
        data.extend(self._overhead_row(result.agc))
        # Guard
        data.extend(self._overhead_row(result.guard))
        # S-SSB
        data.extend(self._overhead_row(result.s_ssb))
        # Total
        data.append(result.overhead_total)

        return data


# Key functions for sorting data
def _result_row_harq_key(row: ResultRow) -> int:
    return row.harq_mode.value


def _result_row_blind_retransmissions_key(row: ResultRow) -> int:
    if row.blind_retransmissions:
        return row.blind_retransmissions
    return 0


def _result_row_feedback_channel_period_key(row: ResultRow) -> int:
    if row.feedback_channel_period:
        return row.feedback_channel_period
    return 0


class ResultTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRow] = []
        self._run_index = 0

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(NrTableColumn)

    def sort(self, column: int, order: Qt.SortOrder = ...):
        # Row number is entirely based on the sorting order,
        # so it doesn't make sense to sort on th
        if column == NrTableColumn.ROW_NUMBER.value:
            return

        self.beginResetModel()
        reverse = order is Qt.SortOrder.AscendingOrder
        if column == NrTableColumn.RUN_INDEX.value:
            self._results.sort(key=attrgetter('run'), reverse=reverse)
        elif column == NrTableColumn.NUMEROLOGY.value:
            self._results.sort(key=attrgetter('numerology'), reverse=reverse)
        elif column == NrTableColumn.RESOURCE_BLOCKS.value:
            self._results.sort(key=attrgetter('resource_blocks'), reverse=reverse)
        elif column == NrTableColumn.LAYERS.value:
            self._results.sort(key=attrgetter('layers'), reverse=reverse)
        elif column == NrTableColumn.UE_MAX_MODULATION.value:
            self._results.sort(key=attrgetter('max_modulation'), reverse=reverse)
        elif column == NrTableColumn.HARQ_MODE.value:
            self._results.sort(key=_result_row_harq_key, reverse=reverse)
        elif column == NrTableColumn.BLIND_TRANSMISSIONS.value:
            self._results.sort(key=_result_row_blind_retransmissions_key, reverse=reverse)
        elif column == NrTableColumn.FEEDBACK_CHANNEL_PERIOD.value:
            self._results.sort(key=_result_row_feedback_channel_period_key, reverse=reverse)
        elif column == NrTableColumn.DATA_RATE.value:
            self._results.sort(key=attrgetter('result'), reverse=reverse)

        self._update_row_numbers()
        self.endResetModel()

    def _update_row_numbers(self):
        for index, result in enumerate(self._results):
            result.row = index

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:

        if role == Qt.DisplayRole:
            result = self._results[index.row()]
            if index.column() == NrTableColumn.ROW_NUMBER.value:
                return result.row
            elif index.column() == NrTableColumn.RUN_INDEX.value:
                return result.run
            elif index.column() == NrTableColumn.NUMEROLOGY.value:
                return result.numerology
            elif index.column() == NrTableColumn.RESOURCE_BLOCKS.value:
                return result.resource_blocks
            elif index.column() == NrTableColumn.LAYERS.value:
                return result.layers
            elif index.column() == NrTableColumn.UE_MAX_MODULATION.value:
                return str(result.max_modulation) + "QAM"
            elif index.column() == NrTableColumn.HARQ_MODE.value:
                if result.harq_mode == HarqMode.BLIND_TRANSMISSION:
                    return "Blind Transmission"
                elif result.harq_mode == HarqMode.FEEDBACK:
                    return "Feedback"
                else:
                    raise ValueError("Unsupported HARQ Mode")
            elif index.column() == NrTableColumn.BLIND_TRANSMISSIONS.value:
                if result.harq_mode == HarqMode.BLIND_TRANSMISSION:
                    return result.blind_retransmissions
                else:
                    return "N/A"
            elif index.column() == NrTableColumn.FEEDBACK_CHANNEL_PERIOD.value:
                if result.harq_mode == HarqMode.FEEDBACK:
                    return result.feedback_channel_period
                else:
                    return "N/A"
            elif index.column() == NrTableColumn.DATA_RATE.value:
                return result.nr_result.data_rate

        if role == Qt.TextAlignmentRole:
            if index.column() != NrTableColumn.HARQ_MODE.value:
                return int(Qt.AlignVCenter) | int(Qt.AlignRight)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(section == NrTableColumn.DATA_RATE.value)
            return font

        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section == 0:
            return str(NrTableColumn.ROW_NUMBER)
        elif section == 1:
            return str(NrTableColumn.RUN_INDEX)
        elif section == 2:
            return str(NrTableColumn.NUMEROLOGY)
        elif section == 3:
            return str(NrTableColumn.RESOURCE_BLOCKS)
        elif section == 4:
            return str(NrTableColumn.LAYERS)
        elif section == 5:
            return str(NrTableColumn.UE_MAX_MODULATION)
        elif section == 6:
            return str(NrTableColumn.HARQ_MODE)
        elif section == 7:
            return str(NrTableColumn.BLIND_TRANSMISSIONS)
        elif section == 8:
            return str(NrTableColumn.FEEDBACK_CHANNEL_PERIOD)
        elif section == 9:
            return str(NrTableColumn.DATA_RATE)

    def append(self, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
               harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
               feedback_channel_period: Optional[int]):
        new_result = ResultRow(
            row=len(self._results),
            run=self._run_index,
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
        self._run_index += 1

    def remove(self, rows: List[int]):
        # Sort descending, so we don't change higher indexes
        # when removing lower rows
        rows.sort(reverse=True)

        # We need a full reset since we update the row numbers too
        self.beginResetModel()
        for row in rows:
            del self._results[row]

        self._update_row_numbers()
        self.endResetModel()

    def reset(self):
        self.beginResetModel()
        self._results = []
        self._run_index = 0
        self.endResetModel()

    def results(self):
        return self._results

    def get_result(self, row: int) -> ResultRow:
        return self._results[row]


def _sort_order_changed_nr(index, order, header: QtWidgets.QHeaderView):
    if index == NrTableColumn.ROW_NUMBER.value:
        header.setSortIndicator(index, Qt.SortOrder.DescendingOrder)


class OverheadTableRow(Enum):
    PSFCH = 0
    PSFCH_PERCENT_TOTAL_OH = 1
    PSFCH_PERCENT_TOTAL = 2
    CSI_RS = 3
    CSI_RS_PERCENT_TOTAL_OH = 4
    CSI_RS_PERCENT_TOTAL = 5
    PT_RS = 6
    PT_RS_PERCENT_TOTAL_OH = 7
    PT_RS_PERCENT_TOTAL = 8
    PSCCH = 9
    PSCCH_PERCENT_TOTAL_OH = 10
    PSCCH_PERCENT_TOTAL = 11
    SCI2 = 12
    SCI2_PERCENT_TOTAL_OH = 13
    SCI2_PERCENT_TOTAL = 14
    DM_RS = 15
    DM_RS_PERCENT_TOTAL_OH = 16
    DM_RS_PERCENT_TOTAL = 17
    AGC = 18
    AGC_PERCENT_TOTAL_OH = 19
    AGC_PERCENT_TOTAL = 20
    GUARD = 21
    GUARD_PERCENT_TOTAL_OH = 22
    GUARD_PERCENT_TOTAL = 23
    S_SSB = 24
    S_SSB_PERCENT_TOTAL_OH = 25
    S_SSB_PERCENT_TOTAL = 26
    TOTAL_OVERHEAD = 27

    def __str__(self) -> str:
        if self is OverheadTableRow.PSFCH:
            return "PSFCH"
        elif self is OverheadTableRow.PSFCH_PERCENT_TOTAL_OH:
            return "PSFCH % Total Overhead"
        elif self is OverheadTableRow.PSFCH_PERCENT_TOTAL:
            return "PSFCH % Total"
        elif self is OverheadTableRow.CSI_RS:
            return "CSI-RS"
        elif self is OverheadTableRow.CSI_RS_PERCENT_TOTAL_OH:
            return "CSI-RS % Total Overhead"
        elif self is OverheadTableRow.CSI_RS_PERCENT_TOTAL:
            return "CSI-RS % Total"
        elif self is OverheadTableRow.PT_RS:
            return "PT-RS"
        elif self is OverheadTableRow.PT_RS_PERCENT_TOTAL_OH:
            return "PT-RS % Total Overhead"
        elif self is OverheadTableRow.PT_RS_PERCENT_TOTAL:
            return "PT-RS % Total"
        elif self is OverheadTableRow.PSCCH:
            return "PSCCH"
        elif self is OverheadTableRow.PSCCH_PERCENT_TOTAL_OH:
            return "PSCCH % Total Overhead"
        elif self is OverheadTableRow.PSCCH_PERCENT_TOTAL:
            return "PSCCH % Total"
        elif self is OverheadTableRow.SCI2:
            return "SCI2"
        elif self is OverheadTableRow.SCI2_PERCENT_TOTAL_OH:
            return "SCI2 % Total Overhead"
        elif self is OverheadTableRow.SCI2_PERCENT_TOTAL:
            return "SCI2 % Total"
        elif self is OverheadTableRow.DM_RS:
            return "DM-RS"
        elif self is OverheadTableRow.DM_RS_PERCENT_TOTAL_OH:
            return "DM-RS % Total Overhead"
        elif self is OverheadTableRow.DM_RS_PERCENT_TOTAL:
            return "DM-RS % Total"
        elif self is OverheadTableRow.AGC:
            return "AGC"
        elif self is OverheadTableRow.AGC_PERCENT_TOTAL_OH:
            return "AGC % Total Overhead"
        elif self is OverheadTableRow.AGC_PERCENT_TOTAL:
            return "AGC % Total"
        elif self is OverheadTableRow.GUARD:
            return "Guard"
        elif self is OverheadTableRow.GUARD_PERCENT_TOTAL_OH:
            return "Guard % Total Overhead"
        elif self is OverheadTableRow.GUARD_PERCENT_TOTAL:
            return "Guard % Total"
        elif self is OverheadTableRow.S_SSB:
            return "S-SSB"
        elif self is OverheadTableRow.S_SSB_PERCENT_TOTAL_OH:
            return "S-SSB % Total Overhead"
        elif self is OverheadTableRow.S_SSB_PERCENT_TOTAL:
            return "S-SSB % Total"
        elif self is OverheadTableRow.TOTAL_OVERHEAD:
            return "Total Overhead"


class OverheadTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._currentResult: Optional[NrResult] = None

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 10

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 3

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignVCenter) | int(Qt.AlignRight)

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
            elif index.column() == 2:
                if index.row() == 0:
                    return self._currentResult.psfch / self._currentResult.resource_total * 100
                elif index.row() == 1:
                    return self._currentResult.csi_rs / self._currentResult.resource_total * 100
                elif index.row() == 2:
                    return self._currentResult.pt_rs / self._currentResult.resource_total * 100
                elif index.row() == 3:
                    return self._currentResult.pscch / self._currentResult.resource_total * 100
                elif index.row() == 4:
                    return self._currentResult.sci2 / self._currentResult.resource_total * 100
                elif index.row() == 5:
                    return self._currentResult.dm_rs / self._currentResult.resource_total * 100
                elif index.row() == 6:
                    return self._currentResult.agc / self._currentResult.resource_total * 100
                elif index.row() == 7:
                    return self._currentResult.guard / self._currentResult.resource_total * 100
                elif index.row() == 8:
                    return self._currentResult.s_ssb / self._currentResult.resource_total * 100
                elif index.row() == 9:
                    return self._currentResult.overhead_total / self._currentResult.resource_total * 100

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

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Overhead Components"
            elif section == 1:
                return "Percent Total Overhead"
            elif section == 2:
                return "Percent Total Resources"

    def set_result(self, nr_result: NrResult):
        self._currentResult = nr_result
        self.dataChanged.emit(QModelIndex(), QModelIndex())


class LteTableColumn(Enum):
    ROW_NUMBER = 0
    RUN_INDEX = 1
    MCS = 2
    RESOURCE_BLOCKS = 3
    PERIOD_SIZE = 4
    PSCCH_SIZE = 5
    DATA_RATE = 6

    def __str__(self):
        if self is LteTableColumn.ROW_NUMBER:
            return "Row"
        elif self is LteTableColumn.RUN_INDEX:
            return "Run Index"
        elif self is LteTableColumn.MCS:
            return "MCS"
        elif self is LteTableColumn.RESOURCE_BLOCKS:
            return "Resource Blocks (PRB)"
        elif self is LteTableColumn.PERIOD_SIZE:
            return "Period Size (subframe)"
        elif self is LteTableColumn.PSCCH_SIZE:
            return "PSCCH Size (subframe)"
        elif self is LteTableColumn.DATA_RATE:
            return "Data Rate (Mb/s)"


class ResultRowLte:
    def __init__(self, row: int, run: int, mcs: int, resource_blocks: int, period_size: int, pscch_size: int,
                 result: float):
        self.row = row
        self.run = run
        self.mcs = mcs
        self.resource_blocks = resource_blocks
        self.period_size = period_size
        self.pscch_size = pscch_size
        self.result = result

    # Match the `LteTableColumn` enum order
    def to_csv(self):
        return [self.row, self.run, self.mcs, self.resource_blocks, self.period_size, self.pscch_size, self.result]


class ResultTableLteModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRowLte] = []
        self._run_index = 0

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(LteTableColumn)

    def _update_row_numbers(self):
        for index, result in enumerate(self._results):
            result.row = index

    def sort(self, column: int, order: Qt.SortOrder = ...):
        # Don't sort the Row number column, since that's just the row's postion
        # in the table
        if column == LteTableColumn.ROW_NUMBER.value:
            return

        self.beginResetModel()
        reverse = order is Qt.SortOrder.AscendingOrder
        if column == 1:
            self._results.sort(key=attrgetter('run'), reverse=reverse)
        elif column == 2:
            self._results.sort(key=attrgetter('mcs'), reverse=reverse)
        elif column == 3:
            self._results.sort(key=attrgetter('resource_blocks'), reverse=reverse)
        elif column == 4:
            self._results.sort(key=attrgetter('period_size'), reverse=reverse)
        elif column == 5:
            self._results.sort(key=attrgetter('pscch_size'), reverse=reverse)
        elif column == 6:
            self._results.sort(key=attrgetter('result'), reverse=reverse)

        self._update_row_numbers()
        self.endResetModel()

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:

        if role == Qt.DisplayRole:
            result = self._results[index.row()]
            if index.column() == LteTableColumn.ROW_NUMBER.value:
                return result.row
            elif index.column() == LteTableColumn.RUN_INDEX.value:
                return result.run
            elif index.column() == LteTableColumn.MCS.value:
                return result.mcs
            elif index.column() == LteTableColumn.RESOURCE_BLOCKS.value:
                return result.resource_blocks
            elif index.column() == LteTableColumn.PERIOD_SIZE.value:
                return result.period_size
            elif index.column() == LteTableColumn.PSCCH_SIZE.value:
                return result.pscch_size
            elif index.column() == LteTableColumn.DATA_RATE.value:
                return result.result

        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignVCenter) | int(Qt.AlignRight)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(section == LteTableColumn.DATA_RATE.value)
            return font

        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section == LteTableColumn.ROW_NUMBER.value:
            return str(LteTableColumn.ROW_NUMBER)
        elif section == LteTableColumn.RUN_INDEX.value:
            return str(LteTableColumn.RUN_INDEX)
        elif section == LteTableColumn.MCS.value:
            return str(LteTableColumn.MCS)
        elif section == LteTableColumn.RESOURCE_BLOCKS.value:
            return str(LteTableColumn.RESOURCE_BLOCKS)
        elif section == LteTableColumn.PERIOD_SIZE.value:
            return str(LteTableColumn.PERIOD_SIZE)
        elif section == LteTableColumn.PSCCH_SIZE.value:
            return str(LteTableColumn.PSCCH_SIZE)
        elif section == LteTableColumn.DATA_RATE.value:
            return str(LteTableColumn.DATA_RATE)

    def append(self, mcs: int, resource_blocks: int, period_size: int, pscch_size: int, result: float):
        new_result = ResultRowLte(
            row=len(self._results),
            run=self._run_index,
            mcs=mcs,
            resource_blocks=resource_blocks,
            period_size=period_size,
            pscch_size=pscch_size,
            result=result
        )

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()
        self._run_index += 1

    def remove(self, rows: List[int]):
        # Sort descending, so we don't change higher indexes
        # when removing lower rows
        rows.sort(reverse=True)

        # We need a full reset since we update the row numbers too
        self.beginResetModel()
        for row in rows:
            del self._results[row]

        self._update_row_numbers()
        self.endResetModel()

    def reset(self):
        self.beginResetModel()
        self._results = []
        self._run_index = 0
        self.endResetModel()

    def results(self):
        return self._results

    def get_result(self, row: int) -> ResultRowLte:
        return self._results[row]


def _sort_order_changed_lte(index, order, header: QtWidgets.QHeaderView):
    if index == LteTableColumn.ROW_NUMBER.value:
        header.setSortIndicator(index, Qt.SortOrder.DescendingOrder)


class ArrowKeyEventFilter(QObject):
    """
    Workaround for not subclassing QTableView for key events
    """

    def __init__(self, table: QtWidgets.QTableView, handler: Callable):
        super(ArrowKeyEventFilter, self).__init__(table)
        self._table = table
        self._table.installEventFilter(self)
        self._handler = handler

    def eventFilter(self, obj, event):
        # Only handle arrow keys
        if obj is self._table and event.type() == QtCore.QEvent.KeyPress and event.key() in (
                QtCore.Qt.Key_Up, QtCore.Qt.Key_Down, Qt.Key_Left, Qt.Key_Right):
            self._handler()

        return super(ArrowKeyEventFilter, self).eventFilter(obj, event)


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

        for possible_value in POSSIBLE_SL_PERIOD_SIZES_LTE:
            self.ui.comboLteSlPeriod.addItem(str(possible_value), userData=possible_value)

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
        self.ui.tableResult.sortByColumn(0, Qt.AscendingOrder)

        self.ui.tableResult.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResult.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableResult.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self._arrow_handler_nr = ArrowKeyEventFilter(self.ui.tableResult, self.selection_changed_nr)

        # Don't show the sort order as descending for the row number
        # since it is entirely dependent on sort order
        self.ui.tableResult.horizontalHeader().sortIndicatorChanged.connect(
            lambda index, order: _sort_order_changed_nr(index=index, order=order,
                                                        header=self.ui.tableResult.horizontalHeader()))

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
        self.ui.tableResultLte.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self._arrow_handler_lte = ArrowKeyEventFilter(self.ui.tableResultLte, self.arrow_key_lte)

        # Don't show the sort order as descending for the row number
        # since it is entirely dependent on sort order
        self.ui.tableResultLte.horizontalHeader().sortIndicatorChanged.connect(
            lambda index, order: _sort_order_changed_lte(index=index, order=order,
                                                         header=self.ui.tableResultLte.horizontalHeader()))

        # Signals
        self.ui.btnCalculate.clicked.connect(self.btn_clicked)
        self.ui.btnToggleOverhead.clicked.connect(self.toggle_overhead_table_clicked)
        self.ui.tableResult.clicked.connect(self.row_clicked_nr)
        self.ui.tableResultLte.clicked.connect(self.row_clicked_lte)
        self.ui.comboNumerology.activated.connect(self.numerology_changed)
        self.ui.comboHarq.activated.connect(self.harq_mode_changed)
        self.ui.btnCalculateLte.clicked.connect(self.btn_clicked_lte)

        self.ui.comboNrChartXAxis.activated.connect(self.replot_chart_nr)
        self.ui.comboNrChartYAxis.activated.connect(self.replot_chart_nr)

        self.ui.comboLteChartXAxis.activated.connect(self.replot_chart_lte)
        self.ui.comboLteChartYAxis.activated.connect(self.replot_chart_lte)

        self.ui.btnClearNr.clicked.connect(self.reset_nr)
        self.ui.btnClearLte.clicked.connect(self.reset_lte)

        self.ui.checkPlotSelectedNr.stateChanged.connect(self.replot_chart_nr)
        self.ui.checkPlotSelectedLte.stateChanged.connect(self.replot_chart_lte)

        # Edit Menu
        self.ui.actionDelete_Selected.triggered.connect(self.delete_from_active_table)
        self.ui.actionClear_Tables.triggered.connect(self.reset_tables)

        # Export Menu
        self.ui.action_CSV.triggered.connect(self.export_csv)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == Qt.Key_Delete:
            self.delete_from_active_table()

        super().keyPressEvent(event)

    def reset_tables(self):
        result = QMessageBox.question(self, "Clear Tables", "Are you sure you want to clear all results")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.reset_nr()
        self.reset_lte()

    def reset_nr(self):
        result = QMessageBox.question(self, "Clear NR Table", "Are you sure you want to clear all NR results")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.tableModel.reset()
        self.replot_chart_nr()

    def reset_lte(self):
        result = QMessageBox.question(self, "Clear LTE Table", "Are you sure you want to clear all LTE results")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.tableModelLte.reset()
        self.replot_chart_lte()

    def delete_from_active_table(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.delete_from_nr()
        elif self.ui.tabWidget.currentIndex() == 1:
            self.delete_from_lte()
        # Index 3 is the charts tab

    def delete_from_nr(self):
        delete_rows = []
        for selected_index in self.ui.tableResult.selectedIndexes():
            # We'll get an index from every selected cell,
            # but we only need the row number,
            # so ignore duplicate row numbers
            if selected_index.row() not in delete_rows:
                delete_rows.append(selected_index.row())
        self.tableModel.remove(delete_rows)
        # Remove the deleted rows from the chart
        self.replot_chart_nr()

    def delete_from_lte(self):
        delete_rows = []
        for selected_index in self.ui.tableResultLte.selectedIndexes():
            # We'll get an index from every selected cell,
            # but we only need the row number,
            # so ignore duplicate row numbers
            if selected_index.row() not in delete_rows:
                delete_rows.append(selected_index.row())
        self.tableModelLte.remove(delete_rows)
        # Remove the deleted rows from the chart
        self.replot_chart_lte()

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
                    headers = list(NrTableColumn)
                    if dialog.ui.checkOverhead.isChecked():
                        headers.extend(list(OverheadTableRow))
                    writer.writerow(headers)
                results = self.tableModel.results()
            else:
                if dialog.ui.checkHeaders.isChecked():
                    writer.writerow(list(LteTableColumn))
                results = self.tableModelLte.results()

            for result in results:
                if selected_table == ExportTable.NR and dialog.ui.checkOverhead.isChecked():
                    writer.writerow(result.to_csv_overhead())
                else:
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
        self.replot_chart_nr()
        # Select the new result
        self.ui.tableResult.selectionModel().select(self.tableModel.index(self.tableModel.rowCount() - 1, 0),
                                                    QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
        # Populate the overhead table with our latest result
        self.tableModelOverHead.set_result(nr_result)

    def value_for_axis(self, result: ResultRow, column: NrTableColumn):
        if column is NrTableColumn.ROW_NUMBER:
            return result.row
        elif column is NrTableColumn.RUN_INDEX:
            return result.run
        elif column is NrTableColumn.NUMEROLOGY:
            return result.numerology
        elif column is NrTableColumn.RESOURCE_BLOCKS:
            return result.resource_blocks
        elif column is NrTableColumn.LAYERS:
            return result.layers
        elif column is NrTableColumn.UE_MAX_MODULATION:
            return result.max_modulation
        elif column is NrTableColumn.HARQ_MODE:
            return result.harq_mode.value
        elif column is NrTableColumn.BLIND_TRANSMISSIONS:
            if result.blind_retransmissions is None:
                return 0
            return result.blind_retransmissions
        elif column is NrTableColumn.FEEDBACK_CHANNEL_PERIOD:
            if result.feedback_channel_period is None:
                return 0
            return result.feedback_channel_period
        elif column is NrTableColumn.DATA_RATE:
            return result.nr_result.data_rate

    def value_for_axis_lte(self, result: ResultRowLte, column: LteTableColumn):
        if column == LteTableColumn.ROW_NUMBER:
            return result.row
        elif column == LteTableColumn.RUN_INDEX:
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
    def replot_chart_nr(self):
        x_value = NrTableColumn(self.ui.comboNrChartXAxis.currentData(Qt.UserRole))
        y_value = NrTableColumn(self.ui.comboNrChartYAxis.currentData(Qt.UserRole))

        series = QtCharts.QLineSeries()

        if self.ui.checkPlotSelectedNr.isChecked():  # plot only selected rows
            visited_rows = []
            for selected_index in self.ui.tableResult.selectedIndexes():
                # We'll get an index from every selected cell,
                # but we only need the row number,
                # so ignore duplicate row numbers
                if selected_index.row() not in visited_rows:
                    visited_rows.append(selected_index.row())
                    result = self.tableModel.get_result(selected_index.row())
                    series.append(self.value_for_axis(result, x_value), self.value_for_axis(result, y_value))
        else:  # Plot all results
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
    def replot_chart_lte(self):
        x_value = LteTableColumn(self.ui.comboLteChartXAxis.currentData(Qt.UserRole))
        y_value = LteTableColumn(self.ui.comboLteChartYAxis.currentData(Qt.UserRole))

        series = QtCharts.QLineSeries()

        if self.ui.checkPlotSelectedLte.isChecked():  # plot only selected rows
            visited_rows = []
            for selected_index in self.ui.tableResultLte.selectedIndexes():
                if selected_index.row() not in visited_rows:
                    visited_rows.append(selected_index.row())
                    result = self.tableModelLte.get_result(selected_index.row())
                    series.append(self.value_for_axis_lte(result, x_value), self.value_for_axis_lte(result, y_value))
        else:
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
        period_size = self.ui.comboLteSlPeriod.currentData(role=Qt.UserRole)
        pscch_size = self.ui.spinPscchSize.value()

        try:
            data_rate = calculate_lte(
                mcs=mcs,
                resource_blocks=resource_blocks,
                period_size=period_size,
                control_channel_size=pscch_size
            )
        except OutOfRangeError as e:
            QMessageBox.critical(self, "Value out of Range", str(e))
            return
        except NotAcceptableValueError as e:
            QMessageBox.critical(self, "Value not acceptable", str(e))
            return
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Value", str(e))
            return

        self.tableModelLte.append(
            mcs=mcs,
            resource_blocks=resource_blocks,
            period_size=period_size,
            pscch_size=pscch_size,
            result=data_rate
        )
        self.replot_chart_lte()
        self.ui.tableResultLte.selectionModel().select(self.tableModelLte.index(self.tableModelLte.rowCount() - 1, 0),
                                                       QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)

    @QtCore.Slot()
    def toggle_overhead_table_clicked(self):
        self.ui.tableOverHead.setVisible(not self.ui.tableOverHead.isVisible())
        if self.ui.tableOverHead.isVisible():
            self.ui.btnToggleOverhead.setText("Hide Overhead")
        else:
            self.ui.btnToggleOverhead.setText("Show Overhead")

    @QtCore.Slot()
    def row_clicked_nr(self, index: QModelIndex):
        self.row_selected_nr(self.tableModel.get_result(index.row()))

    def selection_changed_nr(self):
        self.row_selected_nr(self.tableModel.get_result(self.ui.tableResult.currentIndex().row()))

    def row_selected_nr(self, row: ResultRow):
        self.tableModelOverHead.set_result(row.nr_result)

        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedNr.isChecked():
            self.replot_chart_nr()

    @QtCore.Slot()
    def row_clicked_lte(self, index: QModelIndex):
        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedLte.isChecked():
            self.replot_chart_lte()

    def arrow_key_lte(self):
        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedLte.isChecked():
            self.replot_chart_lte()
