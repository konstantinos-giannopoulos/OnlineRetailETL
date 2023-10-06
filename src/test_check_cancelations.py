import unittest
import pandas as pd
import numpy as np
from cleaning import check_cancelations

class TestCheckCancelations(unittest.TestCase):

    def test_all_cancelations_with_negative_quantities(self):
        # Create a sample DataFrame with cancelation invoices and negative quantities
        data = {'Invoice': ['C001', 'C002', 'C003'],
                'Quantity': [-1, -2, -3]}
        df = pd.DataFrame(data)
        
        # Assert that the result is True
        result = check_cancelations(df)
        self.assertTrue(result)

    def test_not_all_cancelations_with_negative_quantities(self):
        # Create a sample DataFrame with cancelation invoices and a positive quantity
        data = {'Invoice': ['C001', 'C002', 'C003'],
                'Quantity': [-1, -2, 3]}
        df = pd.DataFrame(data)
        
        # Assert that the result is False
        result = check_cancelations(df)
        self.assertFalse(result)

    def test_wrong_argument_type(self):
        # Check if the function raises a TypeError for the wrong argument type
        self.assertRaises(TypeError, check_cancelations, 3)

    def test_missing_columns(self):
        # Create a sample DataFrame with missing 'Invoice' and 'Quantity' columns
        data = {'InvoiceNumber': ['C001', 'C002', 'C003'],
                'Amount': [-1, -2, -3]}
        df = pd.DataFrame(data)
        
        # Check if the function raises a KeyError for missing columns
        self.assertRaises(KeyError, check_cancelations, df)