import unittest
import pandas as pd
import numpy as np
from cleaning import check_neg_quants

class TestCheckNegQuants(unittest.TestCase):

    def test_some_negatives_associated_cancelations(self):
        # Test when some negative quantities are associated with cancelation invoices
        data = {'Invoice': ['C123', 'S456', 'S789', 'C101'],
                'Quantity': [-1, -2, -3, -4]}
        df = pd.DataFrame(data)
        result = check_neg_quants(df)
        self.assertFalse(result)  # Not all negative quantities are associated with cancelation invoices

    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, check_neg_quants, 3)

    def test_no_invoice_quantity_columns(self):
        # Test with a DataFrame missing the 'Invoice' and 'Quantity' columns
        data = {'ID': [1, 2, 3]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, check_neg_quants, df)