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
from core import calculate_nr, HarqMode


def cli_nr(args):
    if "numerology" not in args:
        sys.exit("Argument '--numerology' required in NR mode")

    numerology = args.numerology

    if args.resource_blocks is None:
        if numerology == 0:
            resource_blocks = 52
        elif numerology == 1:
            resource_blocks = 24
        else:  # Just in case...
            sys.exit(f"Unsupported Numerology: {numerology}")
    else:
        resource_blocks = args.resource_blocks

    if args.layers is None:
        sys.exit("Argument '--layers' required in NR mode")

    if args.ue_max_modulation is None:
        sys.exit("Argument '--ue-max-modulation' required in NR mode")

    if args.harq_mode is None:
        sys.exit("Argument '--harq_mode' required in NR mode")

    if args.harq_mode.upper()[0] == 'B':  # BLIND_TRANSMISSION
        harq_mode = HarqMode.BLIND_TRANSMISSION
    elif args.harq_mode[0] == 'F':  # FEEDBACK
        harq_mode = HarqMode.FEEDBACK
    else:  # Shouldn't happen, but just in case
        sys.exit("Error, unsupported HARQ Mode")

    blind_transmissions = None
    feedback_channel_period = None
    if harq_mode == HarqMode.BLIND_TRANSMISSION:
        if args.blind_transmissions is not None:
            blind_transmissions = args.blind_transmissions
        else:
            blind_transmissions = 1
    elif harq_mode == HarqMode.FEEDBACK:
        if args.feedback_channel_period is not None:
            feedback_channel_period = args.feedback_channel_period
        else:
            feedback_channel_period = 1

    data_rate = calculate_nr(numerology=numerology, resource_blocks=resource_blocks, layers=args.layers,
                             ue_max_modulation=args.ue_max_modulation,
                             harq_mode=harq_mode, blind_transmissions=blind_transmissions,
                             feedback_channel_period=feedback_channel_period)

    return data_rate
