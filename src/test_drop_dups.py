import unittest
import pandas as pd
from cleaning import drop_dups

class TestDropDups(unittest.TestCase):

    def test_drop_duplicates_with_default(self):
        # Create a sample DataFrame with duplicates
        data = {
            "ID": [1, 2, 2, 3, 4, 2],
            "Value": ["A", "B", "C", "D", "E", "B"]
        }
        df = pd.DataFrame(data)

        # Call the function with default "last" option
        drop_dups(df)

        # Check if duplicates are dropped with "last" option
        expected_data = {
            "ID": [1, 2, 3, 4, 2],
            "Value": ["A", "C", "D", "E", "B"]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)  # Check if the DataFrame is as expected


    def test_drop_duplicates_with_first_option(self):
        # Create a sample DataFrame with duplicates
        data = {
            "ID": [1, 2, 2, 3, 4, 2],
            "Value": ["A", "B", "C", "D", "E", "B"]
        }
        df = pd.DataFrame(data)

        # Call the function with "first" option
        drop_dups(df, val_to_keep="first")

        # Check if duplicates are dropped with "first" option
        expected_data = {
            "ID": [1, 2, 2, 3, 4],
            "Value": ["A", "B", "C", "D", "E"]
        }
        expected_df = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)  # Check if the DataFrame is as expected


    def test_no_duplicates(self):
        # Create a sample DataFrame without duplicates
        data = {
            "ID": [1, 2, 3, 4],
            "Value": ["A", "B", "C", "D"]
        }
        df = pd.DataFrame(data)

        # Call the function with default "last" option
        drop_dups(df)

        # Check if the DataFrame remains unchanged
        expected_df = df.copy()
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)  # Check if the DataFrame is as expected


    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, drop_dups, 3)


    def test_no_invoice_quantity_columns(self):
        # Test with no valid val_to_keep argument
        data = {'ID': [1, 2, 3], 'Quants': [10, 15, 21]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_dups, df, "all")
