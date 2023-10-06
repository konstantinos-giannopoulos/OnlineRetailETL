import unittest
import pandas as pd

from cleaning import drop_neg_price

class TestDropNegPrice(unittest.TestCase):

    def test_valid_dataframe(self):
        # Test with a valid DataFrame containing negative prices
        data = {'Price': [10, -5, 15, -2, 20]}
        df = pd.DataFrame(data)
        drop_neg_price(df)
        self.assertEqual(len(df), 3)  # Check if rows with negative prices are dropped

    def test_no_negative_prices(self):
        # Test with a DataFrame containing no negative prices
        data = {'Price': [10, 15, 20]}
        df = pd.DataFrame(data)
        drop_neg_price(df)
        self.assertEqual(len(df), 3)  # The DataFrame should remain unchanged

    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, drop_neg_price, 3)

    def test_missing_price_column(self):
        # Test with a DataFrame missing the 'Price' column
        data = {'Amount': [10, 15, 20]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_neg_price, df)
