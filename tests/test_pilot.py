"""Standard-library regression tests for the exploratory mask model."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pilot


class PilotTests(unittest.TestCase):
    def test_each_syndrome_has_two_complementary_masks(self):
        for e in range(8):
            self.assertEqual(pilot.syndrome(e), pilot.syndrome(e ^ 0b111))

    def test_probabilities_sum_to_one(self):
        for b in (0, .01, .02, .04, .08, 1):
            self.assertAlmostEqual(sum(pilot.prob_mask(e, .02, b) for e in range(8)), 1)

    def test_decoder_branch(self):
        s = pilot.syndrome(pilot.BURST)
        self.assertNotEqual(pilot.min_weight_table()[s], pilot.BURST)
        self.assertEqual(pilot.decode_table(.02, .04)[s], pilot.BURST)
        self.assertNotEqual(pilot.decode_table(.02, .01)[s], pilot.BURST)

    def test_exact_known_rates(self):
        base = pilot.min_weight_table()
        informed = pilot.decode_table(.02, .04)
        self.assertAlmostEqual(pilot.exact_failure_rate(.02, 0, base), .001184, places=12)
        self.assertAlmostEqual(pilot.exact_failure_rate(.02, .04, base), .039584, places=12)
        self.assertAlmostEqual(pilot.exact_failure_rate(.02, .04, informed), .02, places=12)

    def test_mc_deterministic_and_counts(self):
        a = pilot.monte_carlo(.02, .04, 3000, 123, pilot.min_weight_table(), pilot.decode_table(.02,.04))
        c = pilot.monte_carlo(.02, .04, 3000, 123, pilot.min_weight_table(), pilot.decode_table(.02,.04))
        self.assertEqual(a, c)
        self.assertEqual(a['shots'], 3000)
        self.assertLessEqual(a['failures_min_weight'], 3000)

if __name__ == '__main__':
    unittest.main()
