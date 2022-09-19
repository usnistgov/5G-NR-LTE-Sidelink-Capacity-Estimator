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

from core import calculate_nr, NrResult, calculate_lte, HarqMode, OutOfRangeError, NotAcceptableValueError, \
    POSSIBLE_SL_PERIOD_SIZES_LTE
import csv
from typing import List, Union, Any, Optional, Callable
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
from PySide6.QtCore import Qt, QObject, QMargins, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QHeaderView, QMessageBox, QDialog, QAbstractButton, QFileDialog
from PySide6.QtCharts import *
from ui_mainwindow import Ui_MainWindow
from ui_csvdialog import Ui_CsvDialog
from enum import Enum
from operator import attrgetter


class ExportTable(Enum):
    """
    Enum for the dropdown in the `CsvDialog`.
    Used to indicate the table the user wants to
    export from
    """
    NR = 0
    LTE = 1


class CsvDialog(QDialog):
    """
    Dialog for the user to configure a comma seperated values (CSV)
    from the application
    """

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
    """
    Representation of each column in the NR Result table.
    These are in order for how they should be presented in
    the application.

    The string representation of this enum should be used whenever
    a given column is displayed to the user
    """
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
            return "Number of Blind Transmissions"
        elif self is NrTableColumn.FEEDBACK_CHANNEL_PERIOD:
            return "Feedback Channel Period (slot)"
        elif self is NrTableColumn.DATA_RATE:
            return "Data Rate (Mb/s)"

    def is_integer_value(self) -> bool:
        return self is NrTableColumn.ROW_NUMBER or \
               self is NrTableColumn.RUN_INDEX or \
               self is NrTableColumn.RESOURCE_BLOCKS or \
               self is NrTableColumn.LAYERS or \
               self is NrTableColumn.BLIND_TRANSMISSIONS or \
               self is NrTableColumn.FEEDBACK_CHANNEL_PERIOD


class ResultRowNr:
    """
    Representation of one calculation displayed on
    the table `tableResult`
    """

    def __init__(self, row: int, run: int, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
                 harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
                 feedback_channel_period: Optional[int]):
        # The index of row on the table. Sensitive to sorting
        self.row = row
        # The unique ID for each calculation. Never changes
        self.run = run

        # User inputs
        self.numerology = numerology
        self.resource_blocks = resource_blocks
        self.layers = layers
        self.max_modulation = max_modulation
        self.harq_mode = harq_mode
        self.nr_result = nr_result
        self.blind_retransmissions = blind_retransmissions
        self.feedback_channel_period = feedback_channel_period

    def to_csv(self):
        # Match the `NrTableColumn` enum order
        return [self.row, self.run, self.numerology, self.resource_blocks, self.layers,
                str(self.max_modulation) + "QAM", str(self.harq_mode), self.blind_retransmissions,
                self.feedback_channel_period, self.nr_result.data_rate]

    def _overhead_row(self, value: float):
        return [value, value / self.nr_result.overhead_total * 100, value / self.nr_result.resource_per_slot * 100]

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
        # Redundant Data
        data.extend(self._overhead_row(result.redundant_data))
        # Total
        data.append(result.overhead_total)

        return data


# Key functions for sorting data
def _result_row_harq_key(row: ResultRowNr) -> int:
    return row.harq_mode.value


def _result_row_blind_retransmissions_key(row: ResultRowNr) -> int:
    if row.blind_retransmissions:
        return row.blind_retransmissions
    return 0


def _result_row_feedback_channel_period_key(row: ResultRowNr) -> int:
    if row.feedback_channel_period:
        return row.feedback_channel_period
    return 0


class ResultTableNrModel(QAbstractTableModel):
    """
    Model for the table `tableResult`, which displays
    the NR results
    """

    def __init__(self):
        super().__init__()
        self._results: List[ResultRowNr] = []
        self._run_index = 0

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(NrTableColumn)

    def sort(self, column: int, order: Qt.SortOrder = ...):
        # We manually define sorting instead of using `QSortFilterProxyModel`
        # so we can easily set the `row` value from its position in the
        # results (`QSortFilterProxyModel` does not reorder data)

        # Row number is entirely based on the sorting order,
        # so it doesn't make sense to sort on it
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
                    return str(HarqMode.BLIND_TRANSMISSION)
                elif result.harq_mode == HarqMode.FEEDBACK:
                    return str(HarqMode.FEEDBACK)
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

        if orientation != Qt.Horizontal or (role != Qt.DisplayRole and role != Qt.ToolTipRole):
            return

        if role == Qt.DisplayRole:
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
        elif role == Qt.ToolTipRole:
            if section == NrTableColumn.UE_MAX_MODULATION.value:
                return "Maximum modulation supported by the UE"

    def append(self, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
               harq_mode: HarqMode, nr_result: NrResult, blind_retransmissions: Optional[int],
               feedback_channel_period: Optional[int]):
        new_result = ResultRowNr(
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

    def get_result(self, row: int) -> ResultRowNr:
        return self._results[row]


def _sort_order_changed_nr(index, order, header: QtWidgets.QHeaderView):
    """
    Helper which stops the sort indicator on the row column
    from being changed, since it will always be descending

    Connected to the `sortIndicatorChanged` signal later
    """
    if index == NrTableColumn.ROW_NUMBER.value:
        header.setSortIndicator(index, Qt.SortOrder.DescendingOrder)


class OverheadTableRow(Enum):
    """
    Representation of each column in the NR Result table.
    These are in order for how they should be presented in
    the application.

    The string representation of this enum should be used whenever
    a given column is displayed to the user.
    """
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
    REDUNDANT_DATA = 27
    REDUNDANT_DATA_TOTAL_OH = 28
    REDUNDANT_PERCENT_TOTAL = 29
    TOTAL_OVERHEAD = 30

    def __str__(self) -> str:
        if self is OverheadTableRow.PSFCH:
            return "PSFCH"
        elif self is OverheadTableRow.PSFCH_PERCENT_TOTAL_OH:
            return "PSFCH Percent Total Overhead (%)"
        elif self is OverheadTableRow.PSFCH_PERCENT_TOTAL:
            return "PSFCH Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.CSI_RS:
            return "CSI-RS"
        elif self is OverheadTableRow.CSI_RS_PERCENT_TOTAL_OH:
            return "CSI-RS Percent Total Overhead (%)"
        elif self is OverheadTableRow.CSI_RS_PERCENT_TOTAL:
            return "CSI-RS Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.PT_RS:
            return "PT-RS"
        elif self is OverheadTableRow.PT_RS_PERCENT_TOTAL_OH:
            return "PT-RS Percent Total Overhead (%)"
        elif self is OverheadTableRow.PT_RS_PERCENT_TOTAL:
            return "PT-RS Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.PSCCH:
            return "PSCCH"
        elif self is OverheadTableRow.PSCCH_PERCENT_TOTAL_OH:
            return "PSCCH Percent Total Overhead (%)"
        elif self is OverheadTableRow.PSCCH_PERCENT_TOTAL:
            return "PSCCH Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.SCI2:
            return "SCI2"
        elif self is OverheadTableRow.SCI2_PERCENT_TOTAL_OH:
            return "SCI2 Percent Total Overhead (%)"
        elif self is OverheadTableRow.SCI2_PERCENT_TOTAL:
            return "SCI2 Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.DM_RS:
            return "DM-RS"
        elif self is OverheadTableRow.DM_RS_PERCENT_TOTAL_OH:
            return "DM-RS Percent Total Overhead (%)"
        elif self is OverheadTableRow.DM_RS_PERCENT_TOTAL:
            return "DM-RS Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.AGC:
            return "AGC"
        elif self is OverheadTableRow.AGC_PERCENT_TOTAL_OH:
            return "AGC Percent Total Overhead (%)"
        elif self is OverheadTableRow.AGC_PERCENT_TOTAL:
            return "AGC Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.GUARD:
            return "Guard"
        elif self is OverheadTableRow.GUARD_PERCENT_TOTAL_OH:
            return "Guard Percent Total Overhead (%)"
        elif self is OverheadTableRow.GUARD_PERCENT_TOTAL:
            return "Guard Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.S_SSB:
            return "S-SSB"
        elif self is OverheadTableRow.S_SSB_PERCENT_TOTAL_OH:
            return "S-SSB Percent Total Overhead (%)"
        elif self is OverheadTableRow.S_SSB_PERCENT_TOTAL:
            return "S-SSB Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.REDUNDANT_DATA:
            return "Redundant Data"
        elif self is OverheadTableRow.REDUNDANT_DATA_TOTAL_OH:
            return "Redundant Data Percent Total Overhead (%)"
        elif self is OverheadTableRow.REDUNDANT_PERCENT_TOTAL:
            return "Redundant Data Percent Total Resource Elements (%)"
        elif self is OverheadTableRow.TOTAL_OVERHEAD:
            return "Total Overhead"


class OverheadTableModel(QAbstractTableModel):
    """
    Model for the table `tableOverHead` in the NR tab.
    Displays the breakdown of overhead components for
    a given `NrResult`
    """

    def __init__(self):
        super().__init__()
        self._currentResult: Optional[NrResult] = None

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 11

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
                    return self._currentResult.redundant_data
                elif index.row() == 10:
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
                    return self._currentResult.redundant_data / self._currentResult.overhead_total * 100
                elif index.row() == 10:
                    return 100.00
            elif index.column() == 2:
                if index.row() == 0:
                    return self._currentResult.psfch / self._currentResult.resource_per_slot * 100
                elif index.row() == 1:
                    return self._currentResult.csi_rs / self._currentResult.resource_per_slot * 100
                elif index.row() == 2:
                    return self._currentResult.pt_rs / self._currentResult.resource_per_slot * 100
                elif index.row() == 3:
                    return self._currentResult.pscch / self._currentResult.resource_per_slot * 100
                elif index.row() == 4:
                    return self._currentResult.sci2 / self._currentResult.resource_per_slot * 100
                elif index.row() == 5:
                    return self._currentResult.dm_rs / self._currentResult.resource_per_slot * 100
                elif index.row() == 6:
                    return self._currentResult.agc / self._currentResult.resource_per_slot * 100
                elif index.row() == 7:
                    return self._currentResult.guard / self._currentResult.resource_per_slot * 100
                elif index.row() == 8:
                    return self._currentResult.s_ssb / self._currentResult.resource_per_slot * 100
                elif index.row() == 9:
                    return self._currentResult.redundant_data / self._currentResult.resource_per_slot * 100
                elif index.row() == 10:
                    return self._currentResult.overhead_total / self._currentResult.resource_per_slot * 100

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
                return "Redundant Data"
            elif section == 10:
                return "Total"

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Average Resource Elements Per Slot"
            elif section == 1:
                return "Percent Total Overhead (%)"
            elif section == 2:
                return "Percent Total Resource Elements (%)"

    def set_result(self, nr_result: NrResult):
        self.beginResetModel()
        self._currentResult = nr_result
        self.endResetModel()

    def reset(self):
        self.beginResetModel()
        self._currentResult = None
        self.endResetModel()


class LteTableColumn(Enum):
    """
    Representation of each column in the LTE Result table.
    These are in order for how they should be presented in
    the application.

    The string representation of this enum should be used whenever
    a given column is displayed to the user
    """
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
            return "Sidelink Period (subframe)"
        elif self is LteTableColumn.PSCCH_SIZE:
            return "PSCCH Length (subframe)"
        elif self is LteTableColumn.DATA_RATE:
            return "Data Rate (Mb/s)"

    def is_integer_value(self) -> bool:
        return self is LteTableColumn.ROW_NUMBER or \
               self is LteTableColumn.RUN_INDEX or \
               self is LteTableColumn.MCS or \
               self is LteTableColumn.RESOURCE_BLOCKS or \
               self is LteTableColumn.PERIOD_SIZE or \
               self is LteTableColumn.PSCCH_SIZE


class ResultRowLte:
    """
    Representation of one calculation displayed on
    the table `tableResultLte`
    """

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
    """
    Model for the table `tableResultLte`, which displays
    the LTE results
    """

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
        # Same justification as `ResultTableNrModel.sort()`
        # We manually define sorting instead of using `QSortFilterProxyModel`
        # so we can easily set the `row` value from its position in the
        # results (`QSortFilterProxyModel` does not reorder data)

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
    """
    Helper which stops the sort indicator on the row column
    from being changed, since it will always be descending

    Connected to the `sortIndicatorChanged` signal later
    """
    if index == LteTableColumn.ROW_NUMBER.value:
        header.setSortIndicator(index, Qt.SortOrder.DescendingOrder)


class ArrowKeyEventFilter(QObject):
    """
    Workaround for not subclassing QTableView for key events.
    Allows for updating the overhead table when the user
    changes the selected row with arrow keys.
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


class ResultRange:
    def __init__(self):
        self.min = 0
        self.max = 0

    def update_range(self, value: int):
        if value < self.min:
            self.min = value
        if value > self.max:
            self.max = value

    def range(self) -> int:
        return int(self.max - self.min)

    def tick_count(self) -> int:
        count = self.range()
        if count < 2:
            return 2
        elif count < 5:
            return count
        return 5


class MainWindow(QMainWindow):
    """
    Model for the overarching window that contains all of our widgets.
    Mostly sets-up, read inputs, & connects signals & slots
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # NR Inputs
        self.ui.comboNumerology.addItem("0", userData=0)
        self.ui.comboNumerology.addItem("1", userData=1)

        self.ui.comboLayers.addItem("1", userData=1)
        self.ui.comboLayers.addItem("2", userData=2)

        self.ui.comboModulation.addItem("64 QAM", userData=64)
        self.ui.comboModulation.addItem("256 QAM", userData=256)

        self.ui.comboHarq.addItem(str(HarqMode.BLIND_TRANSMISSION), userData=HarqMode.BLIND_TRANSMISSION)
        self.ui.comboHarq.addItem(str(HarqMode.FEEDBACK), userData=HarqMode.FEEDBACK)

        self.ui.comboFeedbackChannel.addItem("1", userData=1)
        self.ui.comboFeedbackChannel.addItem("2", userData=2)
        self.ui.comboFeedbackChannel.addItem("4", userData=4)

        # Start NR inputs in a known state
        self.default_nr_inputs()

        # LTE Inputs
        for possible_value in POSSIBLE_SL_PERIOD_SIZES_LTE:
            self.ui.comboLteSlPeriod.addItem(str(possible_value) + " subframes", userData=possible_value)

        # Start LTE inputs in a known state
        self.default_lte_inputs()

        # Charts
        for table_item in list(NrTableColumn):
            self.ui.comboNrChartXAxis.addItem(str(table_item), userData=table_item.value)
            self.ui.comboNrChartYAxis.addItem(str(table_item), userData=table_item.value)
        # Select RUN_INDEX and DATA_RATE as the default X & Y axes
        self.ui.comboNrChartXAxis.setCurrentIndex(
            self.ui.comboNrChartXAxis.findData(NrTableColumn.ROW_NUMBER.value, Qt.UserRole))
        self.ui.comboNrChartYAxis.setCurrentIndex(
            self.ui.comboNrChartYAxis.findData(NrTableColumn.DATA_RATE.value, Qt.UserRole))

        for table_item in list(LteTableColumn):
            self.ui.comboLteChartXAxis.addItem(str(table_item), userData=table_item.value)
            self.ui.comboLteChartYAxis.addItem(str(table_item), userData=table_item.value)
        # Select RUN_INDEX and DATA_RATE as the default X & Y axes
        self.ui.comboLteChartXAxis.setCurrentIndex(
            self.ui.comboLteChartXAxis.findData(LteTableColumn.ROW_NUMBER.value, Qt.UserRole))
        self.ui.comboLteChartYAxis.setCurrentIndex(
            self.ui.comboLteChartYAxis.findData(LteTableColumn.DATA_RATE.value, Qt.UserRole))

        # NR Result table
        self.tableModel = ResultTableNrModel()

        self.ui.tableResult.setModel(self.tableModel)
        self.ui.tableResult.sortByColumn(0, Qt.AscendingOrder)

        self.ui.tableResult.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResult.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableResult.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Install the handler to change the overhead table value when using the arrow keys
        # and update plots if we're only plotting selected values
        self._arrow_handler_nr = ArrowKeyEventFilter(self.ui.tableResult, self.selection_changed_nr)

        # Don't show the sort order as descending for the row number
        # since it is entirely dependent on sort order
        # Use `_sort_order_changed_nr` since Python lambdas
        # may only be one line
        self.ui.tableResult.horizontalHeader().sortIndicatorChanged.connect(
            lambda index, order: _sort_order_changed_nr(index=index, order=order,
                                                        header=self.ui.tableResult.horizontalHeader()))

        # NR Overhead Table
        self.tableModelOverHead = OverheadTableModel()
        self.ui.tableOverHead.setModel(self.tableModelOverHead)
        self.ui.tableOverHead.horizontalHeader().setStretchLastSection(True)
        self.ui.tableOverHead.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # Use the corner button as if it were a header
        # Strictly speaking, it *may* not be there...
        corner_button: QAbstractButton = self.ui.tableOverHead.findChild(QAbstractButton)
        if corner_button:
            # Unfortunately, we can't just add text to this button,
            # So, we add a layout and a label to display text
            button_layout = QtWidgets.QVBoxLayout(corner_button)
            button_layout.setContentsMargins(0, 0, 0, 0)
            label = QtWidgets.QLabel("Overhead Component")
            label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(label)

            # Stretch the vertical header section to fix the text
            # we added earlier
            opt = QtWidgets.QStyleOptionHeader()
            opt.text = label.text()
            size = QtCore.QSize(label.style().sizeFromContents(
                QtWidgets.QStyle.CT_HeaderSection, opt, QtCore.QSize(), label))
            # Give some slight padding to the text
            size.setWidth(size.width() + 10)

            if size.isValid():
                self.ui.tableOverHead.verticalHeader().setMinimumWidth(size.width())

        # LTE Result Table
        self.tableModelLte = ResultTableLteModel()

        self.ui.tableResultLte.setModel(self.tableModelLte)
        self.ui.tableResultLte.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResultLte.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableResultLte.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        # Handle arrow key presses and update plots if we're only plotting selected values
        self._arrow_handler_lte = ArrowKeyEventFilter(self.ui.tableResultLte, self.arrow_key_lte)

        # Don't show the sort order as descending for the row number
        # since it is entirely dependent on sort order
        # Use `_sort_order_changed_lte` since Python lambdas
        # may only be one line
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

        # Clear Table Buttons
        self.ui.btnClearNr.clicked.connect(self.reset_nr)
        self.ui.btnClearLte.clicked.connect(self.reset_lte)

        # Clear Selected Buttons
        self.ui.btnDeleteSelectedNr.clicked.connect(self.delete_from_nr)
        self.ui.btnDeleteSelectedLte.clicked.connect(self.delete_from_lte)

        # Plot Selected Checkboxes
        self.ui.checkPlotSelectedNr.stateChanged.connect(self.replot_chart_nr)
        self.ui.checkPlotSelectedLte.stateChanged.connect(self.replot_chart_lte)

        # Connect Points Checkboxes
        self.ui.checkBoxConnectPointsNr.stateChanged.connect(self.replot_chart_nr)
        self.ui.checkBoxConnectPointsLte.stateChanged.connect(self.replot_chart_lte)

        # Edit Menu
        self.ui.actionDelete_Selected.triggered.connect(self.delete_from_active_table)
        self.ui.actionClear_Tables.triggered.connect(self.reset_tables)

        # Export Menu
        self.ui.action_CSV.triggered.connect(self.export_csv)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """
        Handler allowing results to be deleted with the delete key
        """
        if event.key() == Qt.Key_Delete:
            self.delete_from_active_table()

        super().keyPressEvent(event)

    def default_nr_inputs(self):
        """
        Return all the inputs on the NR tab to their initial state
        """
        self.ui.comboNumerology.setCurrentIndex(self.ui.comboNumerology.findData(0, Qt.UserRole))
        # Trigger this slot manually to change the allowed range of the PRBs
        self.numerology_changed()

        self.ui.spinResourceBlocksNr.setValue(52)
        self.ui.comboLayers.setCurrentIndex(self.ui.comboLayers.findData(2, Qt.UserRole))
        self.ui.comboModulation.setCurrentIndex(self.ui.comboModulation.findData(256, Qt.UserRole))

        self.ui.comboHarq.setCurrentIndex(self.ui.comboHarq.findData(HarqMode.BLIND_TRANSMISSION, Qt.UserRole))
        # Manually trigger this slot, so we only see the relevant inputs for the current HARQ mode
        self.harq_mode_changed()

        self.ui.spinBlindTransmissions.setValue(1)
        self.ui.comboFeedbackChannel.setCurrentIndex(self.ui.comboFeedbackChannel.findData(1, Qt.UserRole))

    def default_lte_inputs(self):
        """
        Return all the inputs on the LTE tab to their initial state
        """
        self.ui.spinMcs.setValue(20)
        self.ui.spinResourceBlocksLte.setValue(50)
        self.ui.comboLteSlPeriod.setCurrentIndex(
            self.ui.comboLteSlPeriod.findData(POSSIBLE_SL_PERIOD_SIZES_LTE[0], Qt.UserRole))
        self.ui.spinPscchSize.setValue(2)

    def reset_tables(self):
        """
        Handler to erase all results and reset all inputs
        """
        result = QMessageBox.question(self, "Clear Tables",
                                      "Are you sure you want to clear all results and reset inputs")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.reset_nr()
        self.reset_lte()

    def reset_nr(self):
        """
        Handler to erase all results and reset all inputs on the NR result table/tab
        """
        result = QMessageBox.question(self, "Clear NR Table",
                                      "Are you sure you want to clear all NR results and reset inputs")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.tableModel.reset()
        self.tableModelOverHead.reset()
        self.replot_chart_nr()
        self.default_nr_inputs()

    def reset_lte(self):
        """
        Handler to erase all results and reset all inputs on the LTE result table/tab
        """
        result = QMessageBox.question(self, "Clear LTE Table",
                                      "Are you sure you want to clear all LTE results and reset inputs")
        if result is not QMessageBox.StandardButton.Yes:
            return
        self.tableModelLte.reset()
        self.replot_chart_lte()
        self.default_lte_inputs()

    def delete_from_active_table(self):
        """
        Handler to delete selected rows
        from the result table on the currently active tab
        """
        if self.ui.tabWidget.currentIndex() == 0:
            self.delete_from_nr()
        elif self.ui.tabWidget.currentIndex() == 1:
            self.delete_from_lte()
        # Index 3 is the charts tab

    def delete_from_nr(self):
        """
        Handler to delete selected rows on the NR result table.
        Also clears the overhead table and resets the NR plot
        """
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

        # Since the currently selected row was probably populating the Overhead Table
        # Reset that as well
        self.tableModelOverHead.reset()

    def delete_from_lte(self):
        """
        Handler to delete selected rows on the LTE result table.
        Also resets the LTE plot
        """
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
        """
        Handler that prompts the user to save results to a CSV file
        """
        dialog = CsvDialog(self)
        if not dialog.exec_():
            return

        if dialog.selected_table() == ExportTable.NR:
            default_filename = "export_NR.csv"
        else:
            default_filename = "export_LTE.csv"
        file = QFileDialog.getSaveFileName(self, caption="Save CSV", dir=default_filename, filter="CSV (*.csv)")
        # No file selected
        if not file[0]:
            return

        # Specify `newline` to avoid extra newlines on Windows
        # See: https://docs.python.org/3/library/csv.html#examples
        with open(file[0], mode='w', newline='', encoding='utf-8') as csv_file:
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
        """
        Handler to update the possible resource blocks when
        the user changes the numerology
        """
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
        """
        Handler that shows the relevant input when the user changes the
        HARQ mode
        """
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
        """
        Handler for when the use clicks the button to calculate the
        data rate on the NR tab
        """
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

    def value_for_axis(self, result: ResultRowNr, column: NrTableColumn):
        """
        Retrieves the appropriate result from a `ResultRowNr`
        for a given `NrTableColumn`
        :param result:
        The result to pull the data from
        :param column:
        The column to match to a field in `result`
        :return:
        The data from `result` that would populate the
        column specified by `column`
        """
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
        """
        Makes the category axis for HARQ values
        :return:
        A `QCategoryAxis` with both HARQ modes mapped to
        their enum values
        """
        category_axis = QCategoryAxis(self)
        category_axis.append(str(HarqMode.BLIND_TRANSMISSION), HarqMode.BLIND_TRANSMISSION.value)
        category_axis.append(str(HarqMode.FEEDBACK), HarqMode.FEEDBACK.value)

        # Streach these slightly longer than needed, so they don't get cut off
        category_axis.setMin(-0.01)
        category_axis.setMax(1.01)
        return category_axis

    @QtCore.Slot()
    def replot_chart_nr(self):
        """
        Regenerates the NR plot based on the users' axis selections
        and NR results
        """
        x_value = NrTableColumn(self.ui.comboNrChartXAxis.currentData(Qt.UserRole))
        y_value = NrTableColumn(self.ui.comboNrChartYAxis.currentData(Qt.UserRole))

        # The default Blue color
        color = QtGui.QColor.fromRgb(32, 159, 223)

        line_series = QLineSeries(self)
        point_series = QScatterSeries(self)
        line_series.setColor(color)
        point_series.setColor(color)

        range_x = ResultRange()
        range_y = ResultRange()

        if self.ui.checkPlotSelectedNr.isChecked():  # plot only selected rows
            visited_rows = []
            for selected_index in self.ui.tableResult.selectedIndexes():
                # We'll get an index from every selected cell,
                # but we only need the row number,
                # so ignore duplicate row numbers
                if selected_index.row() not in visited_rows:
                    visited_rows.append(selected_index.row())
                    result = self.tableModel.get_result(selected_index.row())

                    plot_x = self.value_for_axis(result, x_value)
                    range_x.update_range(plot_x)

                    plot_y = self.value_for_axis(result, y_value)
                    range_y.update_range(plot_y)

                    line_series.append(plot_x, plot_y)
                    point_series.append(plot_x, plot_y)
        else:  # Plot all results
            for result in self.tableModel.results():
                plot_x = self.value_for_axis(result, x_value)
                range_x.update_range(plot_x)
                plot_y = self.value_for_axis(result, y_value)
                range_y.update_range(plot_y)
                line_series.append(plot_x, plot_y)
                point_series.append(plot_x, plot_y)

        chart = self.ui.chartNr.chart()
        chart.removeAllSeries()
        chart.setTitle(f"NR: '{x_value}' - '{y_value}'")
        self.ui.chartNr.set_default_filename(f"NR_{x_value}_{y_value}.png")
        if self.ui.checkBoxConnectPointsNr.isChecked():
            chart.addSeries(line_series)
        chart.addSeries(point_series)

        chart.createDefaultAxes()
        # Use "Nice Numbers" To remove floating point values from
        # integer axes. Also makes floating point representation cleaner
        for axis in chart.axes():
            axis.applyNiceNumbers()

        # Special Handling for HARQ Mode, since those are Enum values
        if x_value == NrTableColumn.HARQ_MODE:
            old_x = chart.axisX()
            point_series.detachAxis(old_x)
            line_series.detachAxis(old_x)
            chart.removeAxis(old_x)

            axis = self.make_harq_axis()
            chart.addAxis(axis, Qt.AlignBottom)
            point_series.attachAxis(axis)
            line_series.attachAxis(axis)
        if y_value == NrTableColumn.HARQ_MODE:
            old_y = chart.axisY()
            point_series.detachAxis(old_y)
            line_series.detachAxis(old_y)
            chart.removeAxis(old_y)

            axis = self.make_harq_axis()
            chart.addAxis(axis, Qt.AlignLeft)
            point_series.attachAxis(axis)
            line_series.attachAxis(axis)

        # For axes that only display integers,
        # do not show decimal points
        if x_value.is_integer_value():
            chart.axisX().setLabelFormat("%i")
            chart.axisX().setTickCount(range_x.tick_count())
        else:
            chart.axisX().setLabelFormat("")
            chart.axisX().setTickCount(5)

        if y_value.is_integer_value():
            chart.axisY().setLabelFormat("%i")
            chart.axisY().setTickCount(range_y.tick_count())
        else:
            chart.axisY().setLabelFormat("")
            chart.axisX().setTickCount(5)

        chart.axisX().setTitleText(str(x_value))
        chart.axisY().setTitleText(str(y_value))

        self.ui.chartNr.setChart(chart)

    @QtCore.Slot()
    def replot_chart_lte(self):
        """
        Regenerates the LTE plot based on the users' axis selections
        and LTE results
        """
        x_value = LteTableColumn(self.ui.comboLteChartXAxis.currentData(Qt.UserRole))
        y_value = LteTableColumn(self.ui.comboLteChartYAxis.currentData(Qt.UserRole))

        # The default Blue color
        color = QtGui.QColor.fromRgb(32, 159, 223)

        line_series = QLineSeries(self)
        point_series = QScatterSeries(self)
        line_series.setColor(color)
        point_series.setColor(color)

        range_x = ResultRange()
        range_y = ResultRange()

        if self.ui.checkPlotSelectedLte.isChecked():  # plot only selected rows
            visited_rows = []
            for selected_index in self.ui.tableResultLte.selectedIndexes():
                if selected_index.row() not in visited_rows:
                    visited_rows.append(selected_index.row())
                    result = self.tableModelLte.get_result(selected_index.row())

                    plot_x = self.value_for_axis_lte(result, x_value)
                    range_x.update_range(plot_x)

                    plot_y = self.value_for_axis_lte(result, y_value)
                    range_y.update_range(plot_y)

                    line_series.append(plot_x, plot_y)
                    point_series.append(plot_x, plot_y)
        else:
            for result in self.tableModelLte.results():
                plot_x = self.value_for_axis_lte(result, x_value)
                range_x.update_range(plot_x)
                plot_y = self.value_for_axis_lte(result, y_value)
                range_y.update_range(plot_y)
                line_series.append(plot_x, plot_y)
                point_series.append(plot_x, plot_y)

        chart = self.ui.chartLte.chart()
        chart.removeAllSeries()
        chart.setTitle(f"LTE: '{x_value}' - '{y_value}'")
        self.ui.chartLte.set_default_filename(f"LTE_{x_value}_{y_value}.png")
        if self.ui.checkBoxConnectPointsLte.isChecked():
            chart.addSeries(line_series)
        chart.addSeries(point_series)

        chart.createDefaultAxes()
        # Use "Nice Numbers" To remove floating point vales from
        # integer axes. Also makes floating point representation cleaner
        for axis in chart.axes():
            axis.applyNiceNumbers()

        # For axes that only display integers,
        # do not show decimal points
        if x_value.is_integer_value():
            chart.axisX().setLabelFormat("%i")
            chart.axisX().setTickCount(range_x.tick_count())
        else:
            chart.axisX().setLabelFormat("")
            chart.axisX().setTickCount(5)

        if y_value.is_integer_value():
            chart.axisY().setLabelFormat("%i")
            chart.axisY().setTickCount(range_y.tick_count())
        else:
            chart.axisY().setLabelFormat("")
            chart.axisX().setTickCount(5)

        chart.axisX().setTitleText(str(x_value))
        chart.axisY().setTitleText(str(y_value))

        self.ui.chartLte.setChart(chart)

    @QtCore.Slot()
    def btn_clicked_lte(self):
        """
        Handler for when the use clicks the button to calculate the
        data rate on the LTE tab
        """
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
        """
        Handler to show/hide the overhead table when the
        user clicks the button above it
        """
        self.ui.tableOverHead.setVisible(not self.ui.tableOverHead.isVisible())
        if self.ui.tableOverHead.isVisible():
            self.ui.btnToggleOverhead.setText("Hide Overhead Components")
        else:
            self.ui.btnToggleOverhead.setText("Show Overhead Components")

    @QtCore.Slot()
    def row_clicked_nr(self, index: QModelIndex):
        """
        Handler for when the user explicitly clicks on a row in the NR table.
        Updates the overhead table
        :see:row_selected_nr
        """
        self.row_selected_nr(self.tableModel.get_result(index.row()))

    def selection_changed_nr(self):
        """
        Handler for when the user changes selection by some other way than clicking.
        Updates the overhead table
        :see:row_selected_nr
        """
        self.row_selected_nr(self.tableModel.get_result(self.ui.tableResult.currentIndex().row()))

    def row_selected_nr(self, row: ResultRowNr):
        """
        Handler to update the overhead table when the user selects a new row
        on the NR result table
        """
        self.tableModelOverHead.set_result(row.nr_result)

        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedNr.isChecked():
            self.replot_chart_nr()

    @QtCore.Slot()
    def row_clicked_lte(self, index: QModelIndex):
        """
        Handler for when the user explicitly clicks on a row in the LTE table.
        Potentially updates the LTE plot
        """
        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedLte.isChecked():
            self.replot_chart_lte()

    def arrow_key_lte(self):
        """
        Handler for when the user uses the arrow keys in the LTE table.
        Potentially updates the LTE plot
        """
        # Trigger a replot if the selection is
        # relevant to the plot
        if self.ui.checkPlotSelectedLte.isChecked():
            self.replot_chart_lte()
