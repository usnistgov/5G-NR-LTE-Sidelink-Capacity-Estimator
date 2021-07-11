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
from enum import Enum
from typing import Optional


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
