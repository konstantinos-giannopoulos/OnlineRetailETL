import sqlite3
from sql import ddl
from sqlalchemy import create_engine


def create_tables():
   conn = sqlite3.connect('./db/invoicedb')
   cursor = conn.cursor()

   # dropping tables if exists
   cursor.execute(ddl.drop_invoice_fact)
   cursor.execute(ddl.drop_stock_dim)
   cursor.execute(ddl.drop_customer_dim)
   cursor.execute(ddl.drop_date_dim)
   conn.execute('PRAGMA foreign_keys = ON;') # enable foreign keys

   #recreating the tables
   cursor.execute(ddl.create_invoice_fact)
   cursor.execute(ddl.create_stock_dim)
   cursor.execute(ddl.create_customer_dim)
   cursor.execute(ddl.create_date_dim)
   
   # commiting
   conn.commit()

   conn.close()
        

def load_db(table_name, df):

   engine = create_engine('sqlite:///db/invoicedb')
   connection = engine.connect()
   
   # load dataframe to db
   df.to_sql(name=table_name, con=connection, if_exists="append", index=False)
