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

import core
import unittest


class CoreNrTests(unittest.TestCase):
    default_numerology = 0
    default_resource_blocks = 52
    default_layers = 2
    default_max_modulation = 256
    default_harq = core.HarqMode.BLIND_TRANSMISSION
    default_blind_transmissions = 1
    default_feedback_channel_period = None

    def test_nr_default_config(self):
        result = core.calculate_nr(numerology=self.default_numerology,
                                   resource_blocks=self.default_resource_blocks,
                                   layers=self.default_layers,
                                   ue_max_modulation=self.default_max_modulation,
                                   harq_mode=self.default_harq,
                                   blind_transmissions=self.default_blind_transmissions,
                                   feedback_channel_period=self.default_feedback_channel_period)

        self.assertAlmostEqual(result.data_rate, 96.776, places=3,
                               msg="Default configuration should produce known value")

    def test_nr_default_overhead(self):
        result = core.calculate_nr(numerology=self.default_numerology,
                                   resource_blocks=self.default_resource_blocks,
                                   layers=self.default_layers,
                                   ue_max_modulation=self.default_max_modulation,
                                   harq_mode=self.default_harq,
                                   blind_transmissions=self.default_blind_transmissions,
                                   feedback_channel_period=self.default_feedback_channel_period)

        self.assertAlmostEqual(result.overhead_total, 2202.6, places=1,
                               msg="Default overhead configuration should produce known value")

    def test_nr_default_overhead_components(self):
        result = core.calculate_nr(numerology=self.default_numerology,
                                   resource_blocks=self.default_resource_blocks,
                                   layers=self.default_layers,
                                   ue_max_modulation=self.default_max_modulation,
                                   harq_mode=self.default_harq,
                                   blind_transmissions=self.default_blind_transmissions,
                                   feedback_channel_period=self.default_feedback_channel_period)

        self.assertAlmostEqual(result.overhead_total,
                               result.psfch + result.pscch +
                               result.csi_rs + result.pt_rs +
                               result.sci2 +
                               result.dm_rs + result.agc + result.guard +
                               result.s_ssb + result.redundant_data,
                               places=1,
                               msg="Overhead total should be the sum of all overhead components")

    def test_nr_zero_overhead_components(self):
        result = core.calculate_nr(numerology=self.default_numerology,
                                   resource_blocks=self.default_resource_blocks,
                                   layers=self.default_layers,
                                   ue_max_modulation=self.default_max_modulation,
                                   harq_mode=self.default_harq,
                                   blind_transmissions=self.default_blind_transmissions,
                                   feedback_channel_period=self.default_feedback_channel_period)
        self.assertEqual(result.csi_rs, 0, msg="`csi_rs` should always be zero")
        self.assertEqual(result.pt_rs, 0, msg="`pt_rs` should always be zero")

    def test_nr_range_numerology(self):
        for good_value in [0, 1]:
            try:
                core.calculate_nr(numerology=good_value,
                                  resource_blocks=24,  # This has to be lowered, since numerology 1 has this limit
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)
            except core.OutOfRangeError:
                self.fail(f"Numerology `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [-1, 2]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Numerology `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_nr(numerology=bad_value,
                                  resource_blocks=24,  # This has to be lowered, since numerology 1 has this limit
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)

    def test_nr_range_resource_blocks(self):
        # Numerology 0
        for good_value in range(11, 53):
            try:
                core.calculate_nr(numerology=0,
                                  resource_blocks=good_value,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)
            except core.OutOfRangeError:
                self.fail(f"Resource blocks: `{good_value}` with numerology `0` should not produce `OutOfRangeError`")

        for bad_value in [10, 53]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Resource blocks: `{bad_value}` " +
                                       "with numerology `0` should produce `OutOfRangeError`"):
                core.calculate_nr(numerology=0,
                                  resource_blocks=bad_value,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)

        # Numerology 1
        for good_value in range(11, 25):
            try:
                core.calculate_nr(numerology=1,
                                  resource_blocks=good_value,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)
            except core.OutOfRangeError:
                self.fail(f"Resource blocks: `{good_value}` with numerology `1` should not produce `OutOfRangeError`")

        for bad_value in [10, 25]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Resource blocks: `{bad_value}` " +
                                       "with numerology `1` should produce `OutOfRangeError`"):
                core.calculate_nr(numerology=1,
                                  resource_blocks=bad_value,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)

    def test_nr_range_layers(self):
        for good_value in [1, 2]:
            try:
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=good_value,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)
            except core.OutOfRangeError:
                self.fail(f"Layers `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [0, 3]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Layers `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=bad_value,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)

    def test_nr_range_modulation(self):
        for good_value in [256, 64]:
            try:
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=self.default_layers,
                                  ue_max_modulation=good_value,
                                  harq_mode=self.default_harq,
                                  blind_transmissions=self.default_blind_transmissions,
                                  feedback_channel_period=self.default_feedback_channel_period)
            except ValueError:
                self.fail(f"UE Max Modulation `{good_value}` should not produce `ValueError`")

        with self.assertRaises(ValueError, msg=f"UE Max Modulation `50` should produce `ValueError`"):
            core.calculate_nr(numerology=self.default_numerology,
                              resource_blocks=self.default_resource_blocks,
                              layers=self.default_layers,
                              ue_max_modulation=50,
                              harq_mode=self.default_harq,
                              blind_transmissions=self.default_blind_transmissions,
                              feedback_channel_period=self.default_feedback_channel_period)

    def test_nr_range_blind_transmissions(self):
        for good_value in range(1, 33):
            try:
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=core.HarqMode.BLIND_TRANSMISSION,
                                  blind_transmissions=good_value,
                                  feedback_channel_period=None)
            except core.OutOfRangeError:
                self.fail(f"Blind Transmissions `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [0, 33]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Blind Transmissions `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=core.HarqMode.BLIND_TRANSMISSION,
                                  blind_transmissions=bad_value,
                                  feedback_channel_period=None)

    def test_nr_range_feedback_channel_period(self):
        for good_value in [1, 2, 4]:
            try:
                core.calculate_nr(numerology=self.default_numerology,
                                  resource_blocks=self.default_resource_blocks,
                                  layers=self.default_layers,
                                  ue_max_modulation=self.default_max_modulation,
                                  harq_mode=core.HarqMode.FEEDBACK,
                                  blind_transmissions=None,
                                  feedback_channel_period=good_value)
            except ValueError:
                self.fail(f"Feedback channel period `{good_value}` should not produce `ValueError`")

        with self.assertRaises(ValueError, msg=f"Feedback channel period `3` should produce `ValueError`"):
            core.calculate_nr(numerology=self.default_numerology,
                              resource_blocks=self.default_resource_blocks,
                              layers=self.default_layers,
                              ue_max_modulation=self.default_max_modulation,
                              harq_mode=core.HarqMode.FEEDBACK,
                              blind_transmissions=None,
                              feedback_channel_period=3)


class CoreLteTests(unittest.TestCase):
    default_mcs = 20
    default_resource_blocks = 50
    default_sidelink_period = 40
    default_pscch_length = 2

    def test_lte_default_config(self):
        data_rate = core.calculate_lte(mcs=self.default_mcs,
                                       resource_blocks=self.default_resource_blocks,
                                       period_size=self.default_sidelink_period,
                                       control_channel_size=self.default_pscch_length)

        self.assertAlmostEqual(data_rate, 4.8114, msg="Default configuration should produce known value")

    def test_lte_range_mcs(self):
        for good_value in range(0, 21):
            try:
                core.calculate_lte(mcs=good_value,
                                   resource_blocks=self.default_resource_blocks,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=self.default_pscch_length)
            except core.OutOfRangeError:
                self.fail(f"MCS value `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [-1, 21]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"MCS value `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_lte(mcs=bad_value,
                                   resource_blocks=self.default_resource_blocks,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=self.default_pscch_length)

    def test_lte_range_resource_blocks(self):
        for good_value in range(1, 111):
            try:
                core.calculate_lte(mcs=self.default_mcs,
                                   resource_blocks=good_value,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=self.default_pscch_length)
            except core.OutOfRangeError:
                self.fail(f"Resource blocks value `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [0, 111]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"Resource blocks  value `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_lte(mcs=self.default_mcs,
                                   resource_blocks=bad_value,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=self.default_pscch_length)

    def test_lte_range_period_size(self):
        for good_value in core.POSSIBLE_SL_PERIOD_SIZES_LTE:
            try:
                core.calculate_lte(mcs=self.default_mcs,
                                   resource_blocks=self.default_resource_blocks,
                                   period_size=good_value,
                                   control_channel_size=self.default_pscch_length)
            except core.NotAcceptableValueError:
                self.fail(f"Period size value `{good_value}` should not produce `NotAcceptableValueError`")

        bad_value = 41
        self.assertNotIn(bad_value, core.POSSIBLE_SL_PERIOD_SIZES_LTE,
                         msg=f"Bad test, bad value `{bad_value}` found in acceptable range")

        with self.assertRaises(core.NotAcceptableValueError,
                               msg=f"Period size value `{bad_value}` should produce `OutOfRangeError`"):
            core.calculate_lte(mcs=self.default_mcs,
                               resource_blocks=self.default_resource_blocks,
                               period_size=bad_value,
                               control_channel_size=self.default_pscch_length)

    def test_lte_range_control_channel(self):
        for good_value in range(2, 41):
            try:
                core.calculate_lte(mcs=self.default_mcs,
                                   resource_blocks=self.default_resource_blocks,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=good_value)
            except core.OutOfRangeError:
                self.fail(f"PSCCH value `{good_value}` should not produce `OutOfRangeError`")

        for bad_value in [1, 41]:
            with self.assertRaises(core.OutOfRangeError,
                                   msg=f"PSCCH value `{bad_value}` should produce `OutOfRangeError`"):
                core.calculate_lte(mcs=self.default_mcs,
                                   resource_blocks=self.default_resource_blocks,
                                   period_size=self.default_sidelink_period,
                                   control_channel_size=bad_value)


if __name__ == '__main__':
    unittest.main()
