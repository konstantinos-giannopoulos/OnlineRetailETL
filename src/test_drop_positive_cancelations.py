import unittest
import pandas as pd
import numpy as np

from cleaning import drop_positive_cancelations

class TestDropPositiveCancelations(unittest.TestCase):

    def test_drop_positive_cancelations(self):
        # Test dropping positive cancelation invoices
        data = {'Invoice': ['C123', 'C456', 'C789', 'C101'],
                'Quantity': [-1, -2, 1, 0]}
        df = pd.DataFrame(data)
        df = drop_positive_cancelations(df)
        expected_result = {'Invoice': ['C123', 'C456'], 'Quantity': [-1, -2]}
        expected_df = pd.DataFrame(expected_result)
        pd.testing.assert_frame_equal(df, expected_df)  # Check if the DataFrame is as expected

    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, drop_positive_cancelations, 3)

    def test_no_invoice_quantity_columns(self):
        # Test with a DataFrame missing the 'Invoice' and 'Quantity' columns
        data = {'ID': [1, 2, 3], 'Quants': [10, 15, 21]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_positive_cancelations, df)