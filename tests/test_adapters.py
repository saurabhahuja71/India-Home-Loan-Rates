import importlib
from pathlib import Path
import unittest
import sys
sys.path.insert(0,str(Path(__file__).parents[1]/'scripts'))

class AdapterTests(unittest.TestCase):
    def test_explicit_home_table_selects_home_loan_not_lap(self):
        fixture=(Path(__file__).parent/'fixtures/home_table.html').read_bytes()
        result=importlib.import_module('banks.hdfc').parse(fixture)
        self.assertEqual(result['product'],'HOME_LOAN')
        self.assertEqual(result['rate_min'],7.75)
        self.assertIn('For All Loans',result['source_row'])
        self.assertEqual(result['rate_source_column'],'Interest Rates (% p.a.) — effective range')
    def test_all_initial_adapters_are_separate_modules(self):
        for name in ('sbi','bank_of_baroda','pnb','hdfc','icici','axis','lic_housing','bajaj_housing'):
            self.assertTrue(importlib.import_module('banks.'+name))
