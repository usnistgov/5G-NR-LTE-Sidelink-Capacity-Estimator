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

import math
import sys
from enum import Enum
from typing import List, Optional, Union, Any
import PySide2.QtCore as QtCore
from PySide2.QtCore import Qt, QMargins, QAbstractTableModel, QModelIndex
from PySide2.QtWidgets import QApplication, QMainWindow, QHeaderView, QMessageBox
from ui_mainwindow import Ui_MainWindow
from PySide2.QtCharts import QtCharts


class HarqMode(Enum):
    BLIND_TRANSMISSION = 0
    FEEDBACK = 1


class OutOfRangeError(ValueError):
    def __init__(self, field_name: str, value, minimum, maximum):
        self.field_name = field_name
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(f"Value for field: `{field_name}`: {value} out of range: [{minimum}, {maximum}]")


class ResultRow:
    def __init__(self, run: int, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
                 harq_mode: HarqMode, blind_retransmissions: int, result: float):
        self.run = run
        self.numerology = numerology
        self.resource_blocks = resource_blocks
        self.layers = layers
        self.max_modulation = max_modulation
        self.harq_mode = harq_mode
        self.blind_retransmissions = blind_retransmissions
        self.result = result


class ResultTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRow] = []

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 8

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
                return result.blind_retransmissions
            elif index.column() == 7:
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
            return "Data Rate (Mbps)"

    def append(self, numerology: int, resource_blocks: int, layers: int, max_modulation: int,
               harq_mode: HarqMode, blind_retransmissions: int, result: float):
        new_result = ResultRow(
            run=len(self._results),
            numerology=numerology,
            resource_blocks=resource_blocks,
            layers=layers,
            max_modulation=max_modulation,
            harq_mode=harq_mode,
            blind_retransmissions=blind_retransmissions,
            result=result)

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()


def calculate_nr(numerology: int, resource_blocks: int, layers: int, ue_max_modulation: int,
                 harq_mode: HarqMode, blind_transmissions: Optional[int]) -> float:
    # ----- Range checks -----
    # numerology
    if numerology != 0 and numerology != 1:
        raise OutOfRangeError(field_name="numerology", value=numerology, minimum=0, maximum=1)

    # resource_blocks
    if numerology == 0 and (resource_blocks > 52 or resource_blocks < 11):
        raise OutOfRangeError(field_name="resource_blocks", value=resource_blocks, minimum=11, maximum=52)

    if numerology == 1 and (resource_blocks > 24 or resource_blocks < 11):
        raise OutOfRangeError(field_name="resource_blocks", value=resource_blocks, minimum=11, maximum=11)

    # layers
    if layers != 1 and layers != 2:
        raise OutOfRangeError(field_name="layers", value=layers, minimum=1, maximum=2)

    # ue_support_max_modulation
    if ue_max_modulation != 64 and ue_max_modulation != 256:
        raise ValueError("`ue_max_modulation` May only be 64 or 256")

    # TODO: Only `BLIND_TRANSMISSION` HARQ mode is currently supported
    if harq_mode != HarqMode.BLIND_TRANSMISSION:
        raise ValueError("Only the `BLIND_TRANSMISSION` HARQ mode is currently supported")

    # blind_retransmissions
    if harq_mode == HarqMode.BLIND_TRANSMISSION and (blind_transmissions < 1 or blind_transmissions > 32):
        raise OutOfRangeError(field_name="blind_retransmissions", value=blind_transmissions, minimum=1, maximum=32)

    # ----- Derived values -----

    if ue_max_modulation == 64:
        modulation_order = 6
    elif ue_max_modulation == 256:
        modulation_order = 8
    else:
        # Shouldn't happen, but just in case
        raise ValueError("Unsupported `ue_max_modulation` value")

    # From `Rmax`
    coding_rate = 948 / 1024
    symbol_duration = 1e-3 / (14 * (2 ** numerology))

    # ----- Physical Side Link Control Channel -----

    # ported from:
    # RE_sci1_RB = [10, 12, 15, 20, 25]
    # RE_sci1_sym = [2, 3]
    # re_sci1 = min(RE_sci1_RB) * 12 * min(RE_sci1_sym)
    re_sci1 = 10 * 12 * 2

    sci2_a = 35
    crc = 24
    beta_offset = 1.125
    q_sci2 = 2
    re_sci2 = math.ceil((sci2_a + crc) * beta_offset / (q_sci2 * coding_rate))

    # ----- DMRS, ACG, and Guard symbol -----
    # Calculations simplified using
    # resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    dmrs = resource_blocks * 2 * 6
    agc = resource_blocks * 12
    guard = resource_blocks * 12

    # S-SSB
    # number of resource elements for SSB every 160 millisecond

    # Simplified using
    # resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    ssb = resource_blocks * 14 * 12

    # average number of resource elements for SSB per slot
    # Simplified from: 1 / (2 ** u) given u = 0
    slot_duration_in_milliseconds = 1

    ssb_per_millisecond = ssb / 160
    ssb_per_slot = ssb_per_millisecond * slot_duration_in_milliseconds

    # Overhead Ratio
    # Both below simplified using: resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    resource_total = blind_transmissions * resource_blocks * 14 * 12
    overhead_total = re_sci1 + re_sci2 + dmrs + agc + guard + ssb_per_slot + (
            blind_transmissions - 1) * resource_blocks * 14 * 12

    overhead_ratio = overhead_total / resource_total

    # removed scaling factor (`f`)
    # simplified using: resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    # original: data_rate = 1e-6 * v_layers * Qm * f * Rmax * NRB_bw_u * 12 * (1 - OH) / Tu
    data_rate = 1e-6 * layers * modulation_order * coding_rate * resource_blocks * 12 * (
            1 - overhead_ratio) / symbol_duration

    return data_rate


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

        self.ui.comboHarq.addItem("Blind Transmission", HarqMode.BLIND_TRANSMISSION)
        self.ui.comboHarq.addItem("Feedback Channel", HarqMode.FEEDBACK)

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

        # Result table

        self.tableModel = ResultTableModel()
        self.ui.tableResult.setModel(self.tableModel)
        self.ui.tableResult.horizontalHeader().setStretchLastSection(True)
        self.ui.tableResult.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)

        # Signals
        self.ui.btnCalculate.clicked.connect(self.btn_clicked)
        self.ui.comboNumerology.activated.connect(self.numerology_changed)

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
    def btn_clicked(self):
        numerology = int(self.ui.comboNumerology.currentData(Qt.UserRole))
        resource_blocks = self.ui.spinResourceBlocks.value()
        layers = int(self.ui.comboLayers.currentData(Qt.UserRole))
        max_modulation = int(self.ui.comboModulation.currentData(Qt.UserRole))
        harq_mode = self.ui.comboHarq.currentData(Qt.UserRole)
        blind_retransmissions = self.ui.spinBlindRetransmissions.value()

        try:
            data_rate = calculate_nr(numerology=numerology, resource_blocks=resource_blocks, layers=layers,
                                     ue_max_modulation=max_modulation,
                                     harq_mode=harq_mode, blind_transmissions=blind_retransmissions)
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
            blind_retransmissions=blind_retransmissions,
            result=data_rate,
        )
        self.series.barSets()[0].insert(0, data_rate)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
