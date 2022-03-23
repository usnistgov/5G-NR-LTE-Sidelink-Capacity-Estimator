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

import sys
from argparse import ArgumentParser
from gui import MainWindow
from cli import cli_nr, cli_lte
from core import OutOfRangeError, calculate_lte
from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    calculate_lte(mcs=20, resource_blocks=50, period_size=40, control_channel_size=2)

    parser = ArgumentParser()

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-c", "--cli", help="Run the program in CLI mode", action="store_true")
    mode_group.add_argument("-g", "--gui", help="Run the program showing the GUI. Ignores all other arguments",
                            action="store_true")

    nr_lte_group = parser.add_mutually_exclusive_group()
    nr_lte_group.add_argument("-n", "--nr", help="Perform the calculation for NR", action="store_true")
    nr_lte_group.add_argument("-l", "--lte", help="Perform the calculation for LTE", action="store_true")

    # Shared Args
    parser.add_argument("--resource-blocks", type=int)

    # NR Args
    parser.add_argument("--numerology", choices=[0, 1], type=int)
    parser.add_argument("--layers", choices=[1, 2], type=int)
    parser.add_argument("--ue-max-modulation", choices=[64, 256], type=int)
    parser.add_argument("--harq-mode", choices=["B", "Blind", "BlindTransmission", "Blind_Transmission",
                                                "F", "Feedback", "FeedbackChannel", "Feedback_Channel"], type=str)
    parser.add_argument("--blind-transmissions", type=int)
    parser.add_argument("--feedback-channel-period", choices=[1, 2, 4], type=int)

    # LTE Args
    parser.add_argument("--mcs", type=int)
    parser.add_argument("--period-size", type=int)
    parser.add_argument("--control-channel-size", type=int)

    args = parser.parse_args()

    if args.cli:
        try:
            if args.nr:
                data_rate = cli_nr(args)
            else:
                data_rate = cli_lte(args)
        except OutOfRangeError as e:
            sys.exit("Out of range error: " + str(e))
        except ValueError as e:
            sys.exit("Value error: " + str(e))

        print(f"Data rate: {data_rate} Mb/s")
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        app.exec_()
