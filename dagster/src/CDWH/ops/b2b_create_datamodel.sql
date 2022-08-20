CREATE OR REPLACE DATABASE CDWH COMMENT = "Customer DWH Demo Project";
CREATE OR REPLACE SCHEMA CORE;

CREATE OR REPLACE WAREHOUSE CDWH_WH WAREHOUSE_SIZE='SMALL';

CREATE OR REPLACE TABLE COMPANIES (
    ID VARCHAR(32) PRIMARY KEY NOT NULL,
    CUIT VARCHAR(32) NOT NULL,
    NAME VARCHAR(64) NOT NULL
);

CREATE OR REPLACE TABLE CUSTOMERS (
    ID VARCHAR(32) PRIMARY KEY NOT NULL,
    NAME VARCHAR(64) NOT NULL,
    DATE_OF_BIRTH DATE
);

CREATE OR REPLACE TABLE PRODUCTS (
    ID VARCHAR(32) PRIMARY KEY NOT NULL,
    NAME VARCHAR(64) NOT NULL
);

CREATE OR REPLACE TABLE CATALOGS (
    VENDOR_COMPANY VARCHAR(32) REFERENCES COMPANIES(ID) NOT NULL,
    PRODUCT VARCHAR(32) REFERENCES PRODUCTS(ID) NOT NULL,
    SUPPLIER_COMPANY VARCHAR(32) REFERENCES COMPANIES(ID) NOT NULL,
    SUPPLIER_PRICE DECIMAL(10,2) NOT NULL,
    RETAIL_PRICE DECIMAL(10,2) NOT NULL,
    VALID_FROM DATE DEFAULT NULL,
    VALID_TO DATE DEFAULT NULL,
    primary key("VENDOR_COMPANY", "PRODUCT")
);

--customer orders only; back-to-back orders of vendors to suppliers are not captured
CREATE OR REPLACE TABLE ORDERS (
    ID VARCHAR(32) PRIMARY KEY,
    TRANSACTION_TIMESTAMP TIMESTAMP NOT NULL,
    VENDOR_COMPANY VARCHAR(32) REFERENCES COMPANIES(ID) NOT NULL,
    PRODUCT VARCHAR(32) REFERENCES PRODUCTS(ID) NOT NULL,
    CUSTOMER VARCHAR(32) REFERENCES CUSTOMERS(ID) NOT NULL,
    QTY INT NOT NULL,
    TOTAL_AMOUNT DECIMAL(10,2) NOT NULL
);

CREATE OR REPLACE TABLE IP_COUNTRY_CACHE (
    IP VARCHAR(15) PRIMARY KEY,
    COUNTRY_CODE VARCHAR(3),
    COUNTRY VARCHAR(255),
    MESSAGE VARCHAR(255),
    DATE_REFRESHED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

TRUNCATE TABLE COMPANIES;
TRUNCATE TABLE CUSTOMERS;
TRUNCATE TABLE PRODUCTS;
TRUNCATE TABLE CATALOGS;
TRUNCATE TABLE ORDERS;
TRUNCATE TABLE IP_COUNTRY_CACHE;