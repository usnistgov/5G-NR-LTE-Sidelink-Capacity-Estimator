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

import typing
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCharts import QtCharts


class ExportChartView(QtCharts.QChartView):
    """
    A wrapper class around `QChartView`
    removing margins and allowing for saving &
    copying to the clipboard
    """

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        super().__init__(parent)
        self._defaultFileName = 'chart.png'

        # Zero out all possible margins
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.chart().setBackgroundRoundness(0)

        self.chart().setContentsMargins(0, 0, 0, 0)
        self.chart().setMargins(QtCore.QMargins(0, 0, 0, 0))
        self.chart().layout().setContentsMargins(0, 0, 0, 0)

    def set_default_filename(self, value: str) -> None:
        """
        Sets the default name the user is presented with when
        they try and save the chart

        :param value:
        The string (with an image extension) for the file.
        """
        # Remove special characters in "Data Rate (Mb/s)"
        for char in " ()/":
            value = value.replace(char, "_")
        self._defaultFileName = value

    def save_as_image(self) -> None:
        """
        Opens a file dialog and prompts the user to save the chart as some image
        """
        image = self.grab()
        (file_name, _) = QtWidgets.QFileDialog.getSaveFileName(self, "Save Chart As Image", self._defaultFileName,
                                                               "Images (*.png *.jpg *.bmp)")
        if not file_name:
            return

        if file_name.lower().endswith(('.bmp', '.jpg', '.jpeg', '.png',)):
            image.save(file_name)
        else:
            image.save(file_name + '.png')

    def copy_to_clipboard(self) -> None:
        """
        Copies the chart to the clipboard
        """
        QtGui.QGuiApplication.clipboard().setPixmap(self.grab())

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QtWidgets.QMenu(self)
        menu.addAction("Save As Image", self.save_as_image)
        menu.addAction("Copy to Clipboard", self.copy_to_clipboard)
        menu.exec_(event.globalPos())
