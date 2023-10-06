import unittest
import pandas as pd

from cleaning import drop_zero_quants

class TestDropZeroQuants(unittest.TestCase):

    def test_drop_zero_quantities(self):
        # Define a sample DataFrame with Quantity column
        data = {'Item': ['A', 'B', 'C', 'D'],
                'Quantity': [10, 0, 5, 0]}
        df = pd.DataFrame(data)

        # Call the function to drop zero quantities
        drop_zero_quants(df)

        # Check if rows with zero quantities have been dropped
        self.assertEqual((df['Quantity'] == 0).sum(), 0)


    def test_invalid_argument_type(self):
        self.assertRaises(TypeError, drop_zero_quants, 3)


    def test_missing_required_columns(self):
        # Define a DataFrame missing the required 'Quantity' column
        data = {'Item': ['A', 'B', 'C', 'D']}
        df = pd.DataFrame(data)

        self.assertRaises(KeyError, drop_zero_quants, df)