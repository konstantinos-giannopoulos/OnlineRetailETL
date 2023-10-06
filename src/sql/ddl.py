create_invoice_fact = '''

    CREATE TABLE IF NOT EXISTS InvoiceFact (
       Invoice          integer,
       StockCode        varchar(10),
       DateID           integer,
       CustomerID       char(10),
       Quantity         integer,
       Price            float,
       FOREIGN KEY(StockCode) REFERENCES StockDim(StockCode),
       FOREIGN KEY(DateID) REFERENCES DateDim(DateID),
       FOREIGN KEY(CustomerID) REFERENCES CustomerDim(CustomerID)
	);

    '''


create_stock_dim ='''

    CREATE TABLE IF NOT EXISTS StockDim (
        StockCode       VARCHAR(10) primary key,
        Description     varchar(100)
    );

'''


create_date_dim ='''

    CREATE TABLE IF NOT EXISTS DateDim (
        DateID          integer primary key,
        Year            integer,
        Month           integer,
        Weekday         varchar(9),
        Hour            integer
    );


'''


create_customer_dim ='''

    CREATE TABLE IF NOT EXISTS CustomerDim (
        CustomerID      VARCHAR(10) primary key,
        Country         varchar(50)
    );

'''


drop_invoice_fact = '''
    
    DROP TABLE IF EXISTS InvoiceFact;

'''

drop_stock_dim='''

    DROP TABLE IF EXISTS StockDim;

'''


drop_date_dim='''

    DROP TABLE IF EXISTS DateDim;
    
'''


drop_customer_dim = '''

    DROP TABLE IF EXISTS CustomerDim;

'''