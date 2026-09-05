"""Adversarial obligations for the proposed row-generation account."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('rosetta_row_probe', Path(__file__).parent/'_PLANS/rosetta_row_probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class RowProbeTests(unittest.TestCase):
    def test_one_factor_gain_needs_a_degeneration_rule(self):
        self.assertEqual(probe.matches(dict(zip(probe.FIELDS,['up','same','same','same']))),[])

    def test_partial_transfer_signatures_overlap(self):
        result = probe.matches(dict(zip(probe.FIELDS,['up','down','up','down'])))
        self.assertIn('kali_take_phi',result)
        self.assertIn('arjuna_give_phi',result)

    def test_unknown_and_incomparable_are_not_preserved(self):
        for relation in ['unknown','incomparable']:
            self.assertNotIn('vishnu_preserve',probe.matches(dict.fromkeys(probe.FIELDS,relation)))

    def test_count_does_not_order_the_labels(self):
        self.assertEqual(probe.census()['label_orders_preserving_same_predicates'],5040)

    def test_exact_domain_and_determinism(self):
        c = probe.census()
        self.assertEqual(c,probe.census())
        self.assertEqual(c['comparison_records'],81)
        self.assertEqual(c['unmatched']+c['single_match']+c['multiple_matches'],81)
        self.assertGreater(c['unmatched'],0)
        self.assertGreater(c['multiple_matches'],0)
        with self.assertRaises(ValueError): probe.matches({'self.phi':'up'})

    def test_predicates_survive_separate_increasing_recodings(self):
        def relation(before,after): return 'up' if after>before else 'down' if after<before else 'same'
        before,after = [2,5,4,7],[3,2,6,1]
        signs = dict(zip(probe.FIELDS,map(relation,before,after)))
        # Different increasing mappings per coordinate, not a shared metric.
        maps = [lambda x:x**3,lambda x:2*x+100,lambda x:3*x,lambda x:x**5]
        recoded = {field:relation(f(a),f(b)) for field,f,a,b in zip(probe.FIELDS,maps,before,after)}
        self.assertEqual(probe.matches(signs),probe.matches(recoded))


if __name__=='__main__': unittest.main()
