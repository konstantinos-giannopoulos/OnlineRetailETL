import numpy as np
import pandas as pd
import regex as re
import logging

logger = logging.getLogger()


def drop_invalid_invoice(df:pd.DataFrame) -> None:
    ''' 
    Drops the invalid invoices.
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from invalid invoices

    Returns
    -------
    pd.DataFrame
        The pandas dataframe with only valid invoices
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    invalid_invoice_idx = df[~df['Invoice'].astype(str).str.isdigit()
                             & ~df['Invoice'].astype(str).str.contains('C')] \
                        .index
    df.drop(invalid_invoice_idx, inplace=True)


def check_cancelations(df:pd.DataFrame) -> bool:
    ''' 
    Checks if all cancelations invoices contains negative quantities.
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to check if it's cancelations invoices
        contains only negative quantities

    Returns
    -------
    boolean: True if all cancelation invoice contains negative quantities.
             Elswise returns False
    
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "Quantity"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    # check if all cancelation invoices have negative quantities
    return np.all(df[df['Invoice'].astype(str).str.startswith('C')]['Quantity'].lt(0))


def drop_positive_cancelations(df:pd.DataFrame) -> pd.DataFrame:
    ''' 
   Drops all the cancelation invoices with positive quantities
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from cancelations
        with positive quantities

    Returns
    -------
    pd.DataFrame:
        A DattaFrame without cancelation invoices with positive quantities
    
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "Quantity"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    df = df.drop(df[df['Invoice'].astype(str).str.contains('C') \
                            & df['Quantity'].ge(0)
              ] \
              .index
            )
    
    return df


def check_neg_quants(df:pd.DataFrame) -> bool:
    ''' 
    Checks if all negative quantities are associated with cancelation invoices.
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to check if it's negative quantities
        are only associated with cancelation invoices.

    Returns
    -------
    boolean: True if all negative quantities are associated with cancelation invoices.
             Elswise returns False.
    
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "Quantity"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError

    return np.all((df['Quantity'].lt(0)) & (~df['Invoice'].astype(str).str.startswith("C")))


def drop_negative_no_cancelations(df:pd.DataFrame) -> None:
    '''
    Drop cancelations invoices which contains positive quantities.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to check if it's cancelations invoices
        contains only negative quantities

    Returns
    -------
    None: It drops the pd.DataFrame inplace
    
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "Quantity"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    df.drop(df[df['Quantity'].lt(0) \
               & (~df['Invoice'].astype(str).str.startswith("C"))] \
                .index,
                inplace=True
            )


def drop_dups(df:pd.DataFrame, val_to_keep:str = "last") -> None:
    '''
    Drops duplicates.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from duplicates

    val_to_keep: str
        Which duplicated value to keep.
        Default "last"

    Returns
    -------
    None: s
    
    '''

    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    valid_val_to_keep = ["first", "last"]
    
    if val_to_keep not in valid_val_to_keep:
        raise KeyError


    if df.duplicated().sum() > 0:
        logger.info("There are duplicates")
        logger.info(f"Dropping and keeping {val_to_keep}")
        return df.drop_duplicates(keep=val_to_keep, inplace=True)
    else:
        logger.info("There are no duplicates")
        return
    

def drop_zero_quants(df:pd.DataFrame) -> None:
    '''
    Drop invoices with zero quantities.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from the 
        zero quantities

    Returns
    -------
    None: It drops the pd.DataFrame inplace
    
    '''
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Quantity"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    df.drop(df.loc[df['Quantity']==0].index, inplace=True)


def drop_neg_price(df:pd.DataFrame) -> None:
    '''
    Drop invoices with negative prices.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from the 
        negative prices

    Returns
    -------
    None: It drops the pd.DataFrame inplace
    
    '''
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Price"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError

    df.drop(df.loc[df['Price']<0].index, inplace=True)


def drop_null_prices(df:pd.DataFrame) -> None:
    '''
    Drop invoices with null prices.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from the 
        null prices

    Returns
    -------
    None: It drops the pd.DataFrame inplace
    
    '''
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Price"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError

    df.drop(df.loc[df['Price'].isnull()].index, inplace=True)


def replace_null_customer_id(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Replaces null customer ids with a code of the following format:
    Gxxxx, where x is a number.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from the 
        null prices

    Returns
    -------
    pd.DataFrame:
        A new pd.DataFrame without null customer ids
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "CustomerID"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError


    invoice_customer_mapping = {}
    unique_customer_id = 1
    
    # Iterate through the DataFrame
    for index, row in df.iterrows():
        invoice_id = row['Invoice']
        customer_id = row['CustomerID']
        
        # Check if customer_id is null
        if pd.isnull(customer_id):
            # Generate a new customer ID or use an existing one for the same invoice
            if invoice_id in invoice_customer_mapping:
                new_customer_id = invoice_customer_mapping[invoice_id]
            else:
                new_customer_id = f'G{unique_customer_id:04d}'  # Format as G0001, G0002, etc.
                unique_customer_id += 1
            
            # Replace the null customer ID with the generated/assigned one
            df.at[index, 'CustomerID'] = new_customer_id
            
            # Update the mapping
            invoice_customer_mapping[invoice_id] = new_customer_id
    
    return df


def drop_invalid_customers_ids(df: pd.DataFrame) -> None:
    ''' 
    Drops the invalid customers ids.
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from invalid customers ids

    Returns
    -------
    pd.DataFrame
        The pandas dataframe with only valid customers ids
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["CustomerID"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    # get the indexes of the Invoices that are not numeric and contains letters (not c) 
    invalid_cust_idx = df[(df['CustomerID'].astype(str).str.contains(r'[A-Z]', flags=re.IGNORECASE))
                          & (~df['CustomerID'].astype(str).str.startswith('G'))].index
    
    
    df.drop(invalid_cust_idx, inplace=True)



def drop_invalid_stock_cd(df: pd.DataFrame):
    ''' 
    Drops the invalid stock codes.
    
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from invalid stock codes

    Returns
    -------
    pd.DataFrame
        The pandas dataframe with only valid stock codes
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["StockCode"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    # get the indexes of the Stock codes with invalid length 
    inv_len_stock_cd_idx = df[(df["StockCode"].str.len()<5) | (df["StockCode"].str.len()>8)].index
    
    
    df.drop(inv_len_stock_cd_idx, inplace=True)


def drop_null_descr(df:pd.DataFrame) -> None:
    '''
    Drop Stock Codes with null descriptions.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe that we want to clear from the 
        null descriptions

    Returns
    -------
    None: It drops the pd.DataFrame inplace
    
    '''
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Description"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError

    df.drop(df.loc[df['Description'].isnull()].index, inplace=True)


def create_date_cols(df:pd.DataFrame) -> pd.DataFrame:
    '''
    Creates the date columns.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe from which we extract the date columns

    Returns
    -------
    pd.DataFrame:
        A new DataFrame which also contains the following columns:
        DateID, Year, Month, Day, Weekday, Hour    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["InvoiceDate"]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError

    df['DateID'] = df['InvoiceDate'].dt.strftime('%y%m%d%H%M').astype(np.int64)
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['Weekday'] = df['InvoiceDate'].dt.day_name()
    df['Hour'] = df['InvoiceDate'].dt.hour
    #date_dim_df = df[['DateID', 'Year', 'Month', 'Day', 'Weekday', 'Hour']].copy()
    
    return df


def create_date_dim_df(df:pd.DataFrame) -> pd.DataFrame:
    '''
    Creates a dataframe which contain only the date related columns.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe from which we extract the date columns

    Returns
    -------
    pd.DataFrame:
        A new DataFrame with only the date columns    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ['DateID', 'Year', 'Month', 'Day', 'Weekday', 'Hour']
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    
    date_dim_df = df[['DateID', 'Year', 'Month', 'Weekday', 'Hour']].copy()
    
    return date_dim_df


def create_stock_dim_df(df:pd.DataFrame) -> pd.DataFrame:
    '''
    Creates a dataframe which contain only the stock related columns.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe from which we extract the stock related columns

    Returns
    -------
    pd.DataFrame:
        A new DataFrame with only the stock related columns    
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ['StockCode', 'Description']
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError
    

    stock_dim_df = df[['StockCode', 'Description']]

    return stock_dim_df


def to_lowercase(df: pd.DataFrame, *args) -> pd.DataFrame:
    '''
    Convert the requested columns to lowercase

    Parameters
    ----------
    data: pd.DataFrame
        The pandas dataframe that we want to convert its columns to lowercase
    *args:
        The columns that we want to convert to lowercase

    Returns
    -------
    pd.Dataframe: A dataframe with converted to lowercase the requested columns
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    if any(col not in df.columns for col in args):
        raise KeyError


    for col in args:
        df[col] = df[col].str.lower()

    return df


def remove_punctuations(df: pd.DataFrame, *args) -> pd.DataFrame:
    '''
    Remove the punctuations from the requested columns

    Parameters
    ----------
    data: pd.DataFrame
        The pandas dataframe that we want to remove the punctuations
    *args:
        The columns that we want to remove the punctuations

    Returns
    -------
    pd.Dataframe: A dataframe with removed punctuations from the requested columns
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    if any(col not in df.columns for col in args):
        raise KeyError
    
    for col in args:
        df.loc[:,col] = df[col].replace(to_replace=r'[^\w\s]', value='', regex=True)

    return df


def remove_unessecary_spaces(df: pd.DataFrame, *args):
    '''
    Remove unessecary spaces from the requested columns

    Parameters
    ----------
    data: pd.DataFrame
        The pandas dataframe that we want to remove the unessecary spaces
    
    *args:
        The columns that we want to remove the unessecary spaces

    Returns
    -------
    pd.Dataframe: A dataframe with removed unessecary spaces from the requested columns
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    if any(col not in df.columns for col in args):
        raise KeyError
    
    for col in args:
        df.loc[:,col] = df[col].replace(to_replace = r'\s+', value = ' ', regex = True).str.strip()

    return df


def create_customer_dim_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Creates a dataframe which contain only the stock related columns.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe from which we extract the customer related columns

    Returns
    -------
    pd.DataFrame:
        A new DataFrame with only the customer related columns  
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ['CustomerID', 'Country']
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError


    customer_dim_df = df[['CustomerID', 'Country']].copy()

    return customer_dim_df


def create_invoice_fct_df(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Drop the columns that are not associated with the InvoiceFact table.
    
    Parameters
    ----------
    df: pd.DataFrame
        The pandas dataframe from which we will keep only the columns that are
        required for the InvoiceFact tables

    Returns
    -------
    pd.DataFrame:
        A new DataFrame with only the associated with the InvoiceFac table columns 
    
    '''
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError
    
    required_columns = ["Invoice", "StockCode",	"Description", "Quantity",
                        "InvoiceDate", "Price", "CustomerID", "Country"
                        ]
    
    if any(column not in df.columns for column in required_columns):
        raise KeyError


    cols_to_drop = ["Description", "InvoiceDate", "Country",
                    "Year", "Month", "Day", "Weekday", "Hour"]
    return df.drop(columns=cols_to_drop)



