import unittest
import pandas as pd
from cleaning import drop_null_prices

class TestDropNullPrices(unittest.TestCase):


    def test_drop_null_prices(self):
        # Create a sample DataFrame for testing
        data = {'Price': [10, None, 15, None, 20]}
        df = pd.DataFrame(data)
        drop_null_prices(df)
        # Check if there are no null prices in the DataFrame
        self.assertFalse(df['Price'].isnull().any())


    def test_drop_null_prices_invalid_input(self):
        self.assertRaises(TypeError, drop_null_prices, 3)


    def test_drop_null_prices_missing_columns(self):
        # Create a DataFrame without the 'Price' column
        data = {'InvalidColumn': [10, None, 15, None, 20]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_null_prices, df)