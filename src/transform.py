import pandas as pd
from cleaning import *


def transform_data(data:pd.DataFrame):

    # Drop invalid Invoices
    logger.info("Dropping Invoices that does not starts with C and are not digits")
    drop_invalid_invoice(data)

    # check if all cancelation invoices contain negative values
    logger.info("Checking if all cancelation invoices contain negative quantity values")
    is_all_cancel_neg = check_cancelations(data)

    # drop the cancelation invoices that contains negative values
    if is_all_cancel_neg == False:
        logger.info("There are cancelation invoices with non negative quantity values.")
        logger.info("Dropping non negative cancelation invoices")
        data = drop_positive_cancelations(data)
    else:
        logger.info("All cancelations invoices contains positive quantities")   


    # check if all negative quantites are associated with cancelations
    logger.info("Checking if all there are negative quantity values in no cancelation invoices")
    is_all_neg_cancel = check_neg_quants(data)


    # drop the rows that contain negative quantities but are not cancelations
    if is_all_neg_cancel == False:
        logger.info("There are negative quantity values that are not associated with cancelation invoices")
        logger.info("Dropping invoices with negative quantities that are not cancelations")
        drop_negative_no_cancelations(data)
    else:
        logger.info("There are no negative quantity values in no cancelation invoices")

    # drop duplicate values if exist
    drop_dups(data)

    # drop rows which contain zero quantities 
    logger.info("Dropping rows with zero quantities")
    drop_zero_quants(data)

    # drop rows which contain negative prices
    logger.info("Dropping rows with negative prices")
    drop_neg_price(data)

    # drop rows which contain negative prices
    logger.info("Dropping rows with null prices")
    drop_null_prices(data)

    # replace null customer id with a code that starts with 'G'
    logger.info("Replacing null customer id with a unique code: Gxxxx")
    data = replace_null_customer_id(data)

    # drop the invalid customer code
    logger.info("Dropping invalid customer codes")
    drop_invalid_customers_ids(data)

    # drop the invalid stock code
    logger.info("Dropping Invalid stock codes")
    drop_invalid_stock_cd(data)

    # drop stockcodes with only null descriptions
    logger.info("Dropping the stock codes that have only null descriptions")
    drop_null_descr(data)

    logger.info("Creating the date dim dataframe")
    # create new columns (Year, Month, Day) in the df
    create_date_cols(data)

    # create date dim DataFrame
    date_dim_df = create_date_dim_df(data)

    # drop duplicate date ids in date dim df
    date_dim_df.drop_duplicates(subset=["DateID"], keep="first", inplace=True)

    logger.info("Date dim dataframe was created")

    logger.info("Creating the stock dim dataframe")
    # create stock dim DataFrame
    stock_dim_df = create_stock_dim_df(data)

    # create a stock dim df with all descriptions converted to lower case
    stock_dim_df = to_lowercase(stock_dim_df, 'Description')

    # # remove punctuations and unessecary spaces to normalize the descriptions
    stock_dim_df = remove_punctuations(stock_dim_df, 'Description')
    stock_dim_df = remove_unessecary_spaces(stock_dim_df, 'Description')

    # drop stock codes with null descriptions
    print(type(stock_dim_df))
    stock_dim_df.dropna(subset=["Description"], inplace=True)

    # drop duplicate stock codes in stock dim df
    stock_dim_df.drop_duplicates(subset=["StockCode"], keep="last",inplace=True)

    logger.info("Stock dim dataframe was created")

    logger.info("Creating customer dim dataframe")
    # create customer dim DataFrame
    customer_dim_df = create_customer_dim_df(data)

    # fill na with Unspecified
    logger.info("Replace null Countries with unspecified")
    customer_dim_df['Country'].fillna("Unspecified", inplace=True)

    # drop duplicates in customer dim DataFrame
    customer_dim_df.drop_duplicates(subset=["CustomerID"], keep="last",inplace=True)

    logger.info("Customer dim dataframe was created")

    logger.info("Creating invoice fact dataframe")
    
    # clear fact table
    invoice_fact = create_invoice_fct_df(data)

    logger.info("Invoice fact dataframe was created")

    # change dtypes of dfs
    

    return invoice_fact, date_dim_df, stock_dim_df, customer_dim_df
