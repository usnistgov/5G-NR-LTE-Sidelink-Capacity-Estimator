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
import lte_values
from enum import Enum
from typing import Optional


class HarqMode(Enum):
    BLIND_TRANSMISSION = 0
    FEEDBACK = 1

    def __str__(self):
        if self is HarqMode.BLIND_TRANSMISSION:
            return "Blind Transmission"
        else:
            return "Feedback"


class OutOfRangeError(ValueError):
    def __init__(self, field_name: str, value, minimum, maximum):
        self.field_name = field_name
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(f"Value for field: `{field_name}`: {value} out of range: [{minimum}, {maximum}]")


class NotAcceptableValueError(ValueError):
    def __init__(self, field_name: str, value, possible_values):
        self.field_name = field_name
        self.value = value
        self.possible_values = possible_values
        super().__init__(f"Value for field: `{field_name}`: {value} not acceptable. Possible values: {possible_values}")


class NrResult:
    def __init__(self, data_rate: float, resource_total: float, psfch: float, pscch: float, sci2: float, dm_rs: float,
                 agc: float, guard: float, s_ssb: float):
        self.resource_total = resource_total
        self.data_rate = data_rate
        self.psfch = psfch
        self.csi_rs = 0
        self.pt_rs = 0
        self.pscch = pscch
        self.sci2 = sci2
        self.dm_rs = dm_rs
        self.agc = agc
        self.guard = guard
        self.s_ssb = s_ssb

        # This excludes `csi_rs` & `pt_rs`, since they're both 0
        self.overhead_total = psfch + pscch + sci2 + dm_rs + agc + guard + s_ssb


def calculate_nr(numerology: int, resource_blocks: int, layers: int, ue_max_modulation: int,
                 harq_mode: HarqMode, blind_transmissions: Optional[int],
                 feedback_channel_period: Optional[int]) -> NrResult:
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

    # blind_transmissions
    if harq_mode == HarqMode.BLIND_TRANSMISSION and (blind_transmissions < 1 or blind_transmissions > 32):
        raise OutOfRangeError(field_name="blind_transmissions", value=blind_transmissions, minimum=1, maximum=32)
    elif harq_mode == HarqMode.FEEDBACK:  # Keep us at one transmission for FEEDBACK mode
        blind_transmissions = 1

    # feedback_channel_period
    if harq_mode == HarqMode.FEEDBACK and (
            feedback_channel_period != 1 and feedback_channel_period != 2 and feedback_channel_period != 4):
        raise ValueError("Feedback Channel Period must be 1, 2, or 4")
    elif harq_mode == HarqMode.BLIND_TRANSMISSION:  # Zero out feedback channel period for BLIND_TRANSMISSION mode
        feedback_channel_period = 0

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

    slot_duration_in_milliseconds = 1 / (2 ** numerology)

    ssb_per_millisecond = ssb / 160
    ssb_per_slot = ssb_per_millisecond * slot_duration_in_milliseconds

    if feedback_channel_period == 0:
        re_feedback = 0
    elif feedback_channel_period == 1:
        re_feedback = resource_blocks * 36
    elif feedback_channel_period == 2:
        re_feedback = resource_blocks * 18
    elif feedback_channel_period == 4:
        re_feedback = resource_blocks * 9
    else:
        raise ValueError(f"Unsupported feedback channel period: {feedback_channel_period}")

    # Overhead Ratio
    # Both below simplified using: resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    resource_total = blind_transmissions * resource_blocks * 14 * 12
    overhead_total = re_sci1 + re_sci2 + dmrs + agc + guard + ssb_per_slot + re_feedback + (
            blind_transmissions - 1) * resource_blocks * 14 * 12

    overhead_ratio = overhead_total / resource_total

    # removed scaling factor (`f`)
    # simplified using: resource_blocks = NRB_bw_u = num_subchan * subchannel_size
    # original: data_rate = 1e-6 * v_layers * Qm * f * Rmax * NRB_bw_u * 12 * (1 - OH) / Tu
    data_rate = 1e-6 * layers * modulation_order * coding_rate * resource_blocks * 12 * (
            1 - overhead_ratio) / symbol_duration

    return NrResult(data_rate=data_rate, resource_total=resource_total, psfch=re_feedback, pscch=re_sci1, sci2=re_sci2,
                    dm_rs=dmrs, agc=agc, guard=guard, s_ssb=ssb_per_slot)


POSSIBLE_SL_PERIOD_SIZES_LTE = [40, 60, 70, 80, 120, 140, 160, 240, 280, 320]


def calculate_lte(mcs: int, resource_blocks: int, period_size: int, control_channel_size: int):
    if mcs < 0 or mcs > 20:
        raise OutOfRangeError(field_name="mcs", value=mcs, minimum=0, maximum=20)

    if resource_blocks < 1 or resource_blocks > 110:
        raise OutOfRangeError(field_name="resource_blocks", value=resource_blocks, minimum=1, maximum=110)

    if period_size not in POSSIBLE_SL_PERIOD_SIZES_LTE:
        raise NotAcceptableValueError(field_name="period_size", value=period_size,
                                      possible_values=POSSIBLE_SL_PERIOD_SIZES_LTE)

    if control_channel_size < 2 or control_channel_size > 40:
        raise OutOfRangeError(field_name="control_channel_size", value=control_channel_size, minimum=2, maximum=40)
    
    if control_channel_size > period_size:
        raise OutOfRangeError(field_name="control_channel_size", value=control_channel_size, minimum=2, maximum=period_size)

    tbs_index = lte_values.mcs_tbs[mcs]

    transport_block_size = lte_values.tbs_prbs[tbs_index][resource_blocks]

    shared_channel_size = period_size - control_channel_size

    # Fixed to 4 in LTE
    harq_tranmissions = 4

    shared_channel_without_harq_subframes = shared_channel_size // harq_tranmissions
    unused_subframes_per_period = shared_channel_size - shared_channel_without_harq_subframes * harq_tranmissions

    capacity_bits_per_period = shared_channel_without_harq_subframes * transport_block_size

    capacity_average_bits = capacity_bits_per_period / period_size

    periods_per_sec = 1 / (period_size / 1000)
    shared_channel_without_harq_subframes_per_sec = math.floor(periods_per_sec) * shared_channel_without_harq_subframes

    last_period_size_in_one_sec_subframes = period_size * (periods_per_sec - math.floor(periods_per_sec))

    pssch_last_period = last_period_size_in_one_sec_subframes
    if last_period_size_in_one_sec_subframes - control_channel_size > 0:
        pssch_last_period = last_period_size_in_one_sec_subframes - control_channel_size

    last_period_without_harq_subframes = math.floor(pssch_last_period / harq_tranmissions)

    total_pssch_subframes_per_second = shared_channel_without_harq_subframes_per_sec + last_period_without_harq_subframes
    capacity_bits_per_second = total_pssch_subframes_per_second * transport_block_size
    average_capacity = capacity_bits_per_period * period_size
    average_phy_capacity = transport_block_size * shared_channel_size * periods_per_sec

    return capacity_bits_per_second * 1e-6
