from extract import *
from transform import transform_data

from load import create_tables, load_db

import logging

logging.basicConfig(filename = '../logs',
                    level = logging.DEBUG,
                    format = " %(levelname)s %(asctime)s - %(message)s "
                    )

logger = logging.getLogger()


def main():

    print("ETL started ...")
    
    # extracting data
    logger.info("Extracting data")
    data = read_data_to_pd()
    logger.info("Data extraction copleted")

    # transforming data
    logger.info("Tranforming data")
    invoice_fact,  date_dim_df, stock_dim_df, customer_dim_df = transform_data(data)
    logger.info("Data transformation completed")


    # creating tables
    logger.info("Creating the tables")
    create_tables()

    # loading data
    logger.info("Loading data into InvoiceFact Table")
    load_db('InvoiceFact', invoice_fact)

    logger.info("Loading data into DateDim Table")
    load_db('DateDim', date_dim_df)

    logger.info("Loading data into StockDim Table")
    load_db('StockDim', stock_dim_df)

    logger.info("Loading data into CustomerDim Table")
    load_db('CustomerDim', customer_dim_df)

    logger.info("Loading of data completed")


    print("ETL finished")



main()

