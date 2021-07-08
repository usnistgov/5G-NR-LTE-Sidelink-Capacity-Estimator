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
from typing import List, Optional, Union, Any
import PySide2.QtCore as QtCore
from PySide2.QtCore import Qt, QMargins, QAbstractTableModel, QModelIndex
from PySide2.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from ui_mainwindow import Ui_MainWindow
from PySide2.QtCharts import QtCharts


class ResultRow:
    def __init__(self, run: Optional[int], result: Optional[float]):
        self.run = run
        self.result = result


class ResultTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._results: List[ResultRow] = []

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self._results)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 2

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex],
             role: int = ...) -> Any:

        if role == Qt.DisplayRole:
            result = self._results[index.row()]
            if index.column() == 0:
                return result.run
            else:
                return result.result

        if role == Qt.TextAlignmentRole:
            if index.column() == 0 or index.column() == 1:
                return Qt.AlignRight  # TODO: AlignVCenter as well

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return

        if section == 0:
            return "Run"
        elif section == 1:
            return "Data Rate (Mbps)"

        return

    def append(self, result: float):
        new_result = ResultRow(len(self._results), result)

        self.beginInsertRows(QModelIndex(), len(self._results), len(self._results))
        self._results.append(new_result)
        self.endInsertRows()


def calculate_nr(mode: str = "unicast", UE_maxQm: int = 64, f: float = 1.0, num_subchan: int = 1,
                 subchannel_size: int = 52) -> float:
    # INPUT CONFIGURATIONS
    # mode = "unicast"  # ["unicast", "groupcast/broadcast"]
    # UE_maxQm = "256 QAM"  # [64 QAM, 256 QAM]
    # UE_maxQm = "64 QAM"  # [64 QAM, 256 QAM]

    # Scaling Factor
    # f = 1

    u = [0, 1]  # ?? numerology for FR1 is 0,1,2; NR n14 band only support first two.

    # number of RBs of BW 10 MHz of different numerologies
    NRB_bw_u_max = [52, 24, 11]
    NRB_bw_u = NRB_bw_u_max[1:len(u)]

    u = 0
    # num_subchan = 1
    # bandwidth part, [11, 52]

    # subchannel_size = 52
    NRB_bw_u = num_subchan * subchannel_size

    if NRB_bw_u > NRB_bw_u_max[u]:
        sys.exit("The assigned RBs are higher than the maximum for Band14.")

    # DETERMINISTIC CONFIGURATIONS

    if mode == "unicast":
        v_layers = 2
        if UE_maxQm == 64:
            Qm = 6
        elif UE_maxQm == 256:
            Qm = 8
        else:
            sys.exit("Unsupported QAM Number")
        Rmax = 948 / 1024
    else:
        v_layers = 1
        # TODO: expand
        Qm = 0
        Rmax = 0

    # Symbol Duration
    Tu = 1e-3 / (14 * (2 ** u))

    # Overhead Radio Calculation

    # Blind Retransmissions
    N_blind_ret = 1

    # PSCCH

    # minimum number of resource elements for PSCCH
    # two symbols, 10 RBs, and 12 RE per RB
    RE_sci1_RB = [10, 12, 15, 20, 25]
    RE_sci1_sym = [2, 3]
    RE_sci1 = min(RE_sci1_RB) * 12 * min(RE_sci1_sym)

    # PSSCH SCI 2

    if mode == "unicast":
        l_sci2 = 35  # SCI2-A
    else:
        l_sci2 = 48  # SCI2-B
    l_crc = 24
    beta_offset = 1.125
    Q_sci2 = 2
    RE_sci2 = math.ceil((l_sci2 + l_crc) * beta_offset / (Q_sci2 * Rmax))

    # DMRS, ACG, and Guard symbol
    RE_dmrs = NRB_bw_u * 2 * 6
    RE_agc = NRB_bw_u * 1 * 12
    RE_guard = NRB_bw_u * 1 * 12

    # S-SSB
    # number of resource elements for SSB every 160 millisecond
    RE_SSB = NRB_bw_u * 14 * 12
    # average number of resource elements for SSB per slot
    slot_duration_in_millisecond = 1 / (2 ** u)
    RE_SSB_per_millisecond = RE_SSB / 160
    RE_SSB_per_slot = RE_SSB_per_millisecond * slot_duration_in_millisecond

    # In case that the assigned subchannels do not cover the 11 RBs for SSB,
    # then there is no SSB OH
    # RE_SSB_per_slot = 0

    # OH ratio
    RE_total = N_blind_ret * NRB_bw_u * 14 * 12
    OH_total = RE_sci1 + RE_sci2 + RE_dmrs + RE_agc + RE_guard + RE_SSB_per_slot + (
            N_blind_ret - 1) * NRB_bw_u * 14 * 12
    OH = OH_total / RE_total
    data_rate = 1e-6 * v_layers * Qm * f * Rmax * NRB_bw_u * 12 * (1 - OH) / Tu

    return data_rate


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.comboBoxMode.addItem("unicast", userData=0)
        self.ui.comboBoxMode.addItem("groupcast/broadcast", userData=1)

        self.ui.comboBoxMaxQm.addItem("64 QAM", userData="64")
        self.ui.comboBoxMaxQm.addItem("256 QAM", userData="256")

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

        # Signals
        self.ui.btnCalculate.clicked.connect(self.btn_clicked)

    @QtCore.Slot()
    def btn_clicked(self):
        qm = int(self.ui.comboBoxMaxQm.currentData(Qt.UserRole))
        scale_factor = float(self.ui.spinScaleFactor.value())
        subchannel_count = int(self.ui.spinSubChannels.value())
        subchannel_size = int(self.ui.spinSubchannelSize.value())

        data_rate = calculate_nr(UE_maxQm=qm, f=scale_factor, num_subchan=subchannel_count,
                                 subchannel_size=subchannel_size)
        self.tableModel.append(data_rate)
        self.series.barSets()[0].insert(0, data_rate)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()

    print(calculate_nr())
