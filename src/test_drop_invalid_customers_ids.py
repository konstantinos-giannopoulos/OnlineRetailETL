import unittest
import pandas as pd

from cleaning import drop_invalid_customers_ids

class TestDropInvalidCustomerIDs(unittest.TestCase):

    def test_valid_customer_ids(self):
        # Test with valid customer IDs (no codes starts with G)
        data = {'CustomerID': ['G123', 'G456', 'G789']}
        df = pd.DataFrame(data)
        drop_invalid_customers_ids(df)
        self.assertEqual(len(df), 3)  # The DataFrame should remain unchanged

    def test_invalid_customer_ids(self):
        # Test with invalid customer IDs (contain at least one letter and not starting with G)
        data = {'CustomerID': ['G123', '12578', 'X789']}
        df = pd.DataFrame(data)
        drop_invalid_customers_ids(df)
        self.assertEqual(len(df), 2)  # The DataFrame should have one row remaining


    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, drop_invalid_customers_ids, 3)

    def test_no_customer_id_column(self):
        # Test with a DataFrame missing the 'Customer ID' column
        data = {'ID': ['123', '456', '789']}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_invalid_customers_ids, df)

