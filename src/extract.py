import zipfile
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger()


def read_data_to_pd(filepath="./data/Invoices_Year_2009-2010.zip") -> pd.DataFrame:
        
        df = pd.read_csv(filepath,
                    header=0,
                    parse_dates=['InvoiceDate'],
                    encoding="iso-8859-1",
                    dtype={'Invoice': str,
                            'StockCode': str,
                            'Description': str,
                            'Quantity': int,
                            'Price': float,
                            'Customer ID': str,
                            'Country': str
                            }
                    )
    
        df.rename(columns={'Customer ID': 'CustomerID'}, inplace=True)
    
        return df


