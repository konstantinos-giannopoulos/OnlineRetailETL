import unittest
import pandas as pd

# Import your function
from cleaning import drop_negative_no_cancelations

class TestDropNegativeNoCancelations(unittest.TestCase):
    
    def test_drop_negative_no_cancelations(self):
        # Create a sample DataFrame
        data = {
            "Invoice": ["A123", "B456", "C789", "D101", "E202"],
            "Quantity": [5, 3, -2, -1, 0]
        }
        df = pd.DataFrame(data)
        
        # Call the function to drop negative no-cancelation invoices
        drop_negative_no_cancelations(df)

        # Check if the result is as expected
        expected_data = {
            "Invoice": ["A123", "B456", "C789", "E202"],
            "Quantity": [5, 3, -2, 0]
        }
        expected_df = pd.DataFrame(expected_data)
        
        pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)  # Check if the DataFrame is as expected

    def test_invalid_dataframe_type(self):
        # Test with an invalid argument type
        self.assertRaises(TypeError, drop_negative_no_cancelations, 3)

    def test_no_invoice_quantity_columns(self):
        # Test with a DataFrame missing the 'Invoice' and 'Quantity' columns
        data = {'ID': [1, 2, 3], 'Quants': [10, 15, 21]}
        df = pd.DataFrame(data)
        self.assertRaises(KeyError, drop_negative_no_cancelations, df)
