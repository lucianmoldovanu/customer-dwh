import setuptools

setuptools.setup(
    name="CUSTOMER_DWH",
    packages=setuptools.find_packages(exclude=["CUSTOMER_DWH_tests"]),
    install_requires=[
        "dagster==0.14.16",
        "dagit==0.14.16",
        "dbt-snowflake",
        "dagster-dbt",
        "pytest",
        "snowflake-connector-python",
        "sqlalchemy",
        "snowflake-sqlalchemy"
    ],
)