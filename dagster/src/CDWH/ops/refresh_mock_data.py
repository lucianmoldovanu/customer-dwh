#!/usr/bin/env python3
import random
import os
import pandas as pd
from sqlalchemy import create_engine
from dagster import Dict, op

from CDWH.utils import random_date

### constants for mock data generation
N_COMPANIES = 100
N_CUSTOMERS = 50

SUPPLIER_PRODUCT_PRICE_RANDOM_MIN = 150
SUPPLIER_PRODUCT_PRICE_RANDOM_MAX = 1500

VENDOR_PROFIT_MARGIN_PERCENT_MIN = 0.2
VENDOR_PROFIT_MARGIN_PERCENT_MAX = 1

@op
def refresh_mock(a) -> Dict:
    engine = create_engine(
        'snowflake://{user}:{password}@{account_identifier}/CUSTOMER_DWH/B2B'.format(
            user=os.environ['SNOWFLAKE_USER'],
            password=os.environ['SNOWFLAKE_PASS'],
            account_identifier=os.environ['SNOWFLAKE_HOST']
        )
    )

    connection = engine.connect()

    ## MOCK DATA: COMPANIES
    pool_company_names = ['Obonoxiuos', 'Clever', 'Phenomenal']
    pool_company_types = ['Company', 'Ltd.', 'Corporation']

    companies = [(
        'C%s' % str(idx+1).rjust(5, '0'),
        random.randint(1000000000, 2000000000),
        ' '.join([
            random.choice(pool_company_names), 
            random.choice(pool_company_names), 
            random.choice(pool_company_types)
        ])
    ) for idx in range(N_COMPANIES)]

    df_companies = pd.DataFrame(
        data = companies,
        columns = ['ID', 'CUIT', 'NAME']
    )

    df_companies.to_sql(
        'companies', 
        con = engine,
        if_exists='append',
        index = False
    )

    companies_suppliers = companies[0:2] #level-1 parts suppliers (i.e. importers)
    companies_purchasers = companies[2:] #level-2 parts suppliers (distributors)

    ## MOCK DATA: PRODUCTS
    # products are defined with reference prices, such that reseller prices can be generates in a reasonable range around the reference price
    products = [
        (
        'P%s' % str(idx+1).rjust(5, '0'),
        prod
        ) for idx, prod in enumerate([
            'Gear lever', 'Seat belt', 'Steering wheel', 'Windscreen', 'Windshield wipers', 'Speedometer', 'Headlights', 'Taillights/Turn signal', 'Hood/Engine', 'Trunk', 'Engine', 'Transmission', 'Battery', 'Alternator', 'Radiator', 'Front Axle', 'Front Steering and Suspension', 'Brakes', 'Catalytic Converter', 'Muffler', 'Fuel gauge', 'Temperature gauge', 'Car trip meter', 'Rev counter', 'Wheel/Tire', 'Tailpipe', 'Fuel Tank', 'Rear Axle', 'Rear Suspension', 'License Plate/Bumper Stickers'
        ])
    ]

    df_products = pd.DataFrame(
        data = products,
        columns = ['ID', 'NAME']
    )

    df_products.to_sql(
        'products', 
        con = engine,
        if_exists='append',
        index = False
    )

    products_with_refprices = [
        (
            p[0],   #product id
            random.randint(SUPPLIER_PRODUCT_PRICE_RANDOM_MIN, SUPPLIER_PRODUCT_PRICE_RANDOM_MAX) #reference price in the 1st level in supply chain (supplier)
        )
        for p in products
    ]
    
    ## MOCK DATA: CATALOGS
    # each purchaser company (distributor) has 10 random parts in the catalog
    # supplier companies don't have catalogs (not captured by mock data)
    catalogs = [
        (
            cp[0],  #VENDOR_COMPANY
            p[0],   #PRODUCT
            random.choice(companies_suppliers)[0],      #SUPPLIER_COMPANY
            p[1],                                       #supplier price
            p[1] * random.uniform(1 + VENDOR_PROFIT_MARGIN_PERCENT_MIN, 1 + VENDOR_PROFIT_MARGIN_PERCENT_MAX)  #RETAIL PRICE includes random relative profit margin on top of supplier price
        ) for cp in companies_purchasers for p in random.sample(products_with_refprices, random.randint(3, 7)) #each retailer has between 3 and 7 products in catalog for sale
    ]

    df_catalogs = pd.DataFrame(
        data = catalogs,
        columns = ['VENDOR_COMPANY', 'PRODUCT', 'SUPPLIER_COMPANY', 'SUPPLIER_PRICE', 'RETAIL_PRICE']
    )

    df_catalogs.to_sql(
        'catalogs', 
        con = engine,
        if_exists='append',
        index = False
    )

    ## MOCK DATA: CUSTOMERS

    pool_first_names = ['Adrienne', 'Makenna', 'Imani', 'Scarlet', 'Ella', 'Angel', 'Zion', 'Emmalee', 'Parker', 'Iliana', 'Joslyn', 'Luz', 'Gabriella', 'Brynlee', 'Giana', 'Amy', 'Charlie', 'Maribel', 'Luna', 'Cameron', 'Madyson', 'Ayla', 'Davis', 'Kade', 'Yahir', 'Patrick', 'Moses', 'Cayden', 'William', 'Ricky', 'Derick', 'Ronald', 'Ricardo', 'Clayton', 'Markus', 'Brody']
    pool_last_names = ['Patrick', 'Terry', 'Daniel', 'Marshall', 'Sparks', 'Hunt', 'Roberts', 'Barrett', 'Cook', 'Roy', 'Joseph', 'Skinner']

    customers = [(
        'CUST%s' % str(idx+1).rjust(5, '0'),
        ' '.join([
            random.choice(pool_first_names), 
            random.choice(pool_last_names)
        ]),
        random_date('1950-01-01', '2000-12-31')
    ) for idx in range(N_CUSTOMERS)]

    df_customers = pd.DataFrame(
        data = customers,
        columns = ['ID', 'NAME', 'DATE_OF_BIRTH']
    )

    df_customers.to_sql(
        'customers', 
        con = engine,
        if_exists='append',
        index = False
    )

    ## MOCK DATA: ORDERS
    # generate between 0 and 5 order for each catalog item
    orders_raw = [
        (   
            random_date('2021-12-01', '2022-03-31') + ' 16:00:00', #transaction_timestamp
            c[0], #vendor company
            c[1], #product
            random.choice(customers)[0], #customer
            random.randint(1, 10), #qty
            c[4] #retail_price
        ) for c in catalogs for i in range(0, random.randint(0, 5))
    ]

    orders = [
        (
            'ORD%s' % str(idx+1000).rjust(5, '0'),
            o[0],
            o[1],
            o[2],
            o[3],
            o[4],
            o[4] * o[5]
        ) for idx, o in enumerate(orders_raw)
    ]

    df_orders = pd.DataFrame(
        data = orders,
        columns = ['ID',  'TRANSACTION_TIMESTAMP', 'VENDOR_COMPANY', 'PRODUCT', 'CUSTOMER', 'QTY', 'TOTAL_AMOUNT']
    )

    df_orders.to_sql(
        'orders', 
        con = engine,
        if_exists='append',
        index = False
    )

    res = {}
    res['customers'] = customers

    connection.close()
    engine.dispose()

    return res