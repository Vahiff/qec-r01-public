import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from calibration import estimate_b_from_ones,run,wilson95

class CalibrationTests(unittest.TestCase):
    def test_estimator_and_clipping(self):
        self.assertEqual(estimate_b_from_ones(0,100),0)
        self.assertEqual(estimate_b_from_ones(100,100),0.08)
        self.assertAlmostEqual(estimate_b_from_ones(584,10000),0.04)
    def test_invalid(self):
        with self.assertRaises(ValueError): estimate_b_from_ones(2,1)
    def test_wilson(self):
        self.assertEqual(wilson95(0,0),[None,None])
        lo,hi=wilson95(195,200)
        self.assertLess(lo,0.975)
        self.assertGreater(hi,0.975)
    def test_deterministic(self):
        x=run(replicates=25,seed=17)
        y=run(replicates=25,seed=17)
        self.assertEqual(x,y)
        self.assertEqual([r['N'] for r in x['results']],[0,50,200,1000,5000])
    def test_no_calibration_baseline(self):
        x=run(replicates=3,seed=3)
        self.assertEqual(x['results'][0]['average_exact_logical_error_rate'],x['exact_minimum_weight_LER'])

if __name__=='__main__': unittest.main()
