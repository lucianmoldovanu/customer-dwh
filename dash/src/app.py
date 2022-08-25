import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from sqlalchemy import Column, String, create_engine

# arguments
SNOWFLAKE_DB = 'CDWH'
SNOWFLAKE_SCHEMA = 'CORE'
SNOWFLAKE_WAREHOUSE = 'CDWH_WH'

connString = 'snowflake://{user}:{password}@{account_identifier}/{db}/{schema}?warehouse={warehouse}'.format(
    user=os.environ['SNOWFLAKE_USER'],
    password=os.environ['SNOWFLAKE_PASS'],
    account_identifier=os.environ['SNOWFLAKE_HOST'],
    db=SNOWFLAKE_DB,
    schema=SNOWFLAKE_SCHEMA,
    warehouse=SNOWFLAKE_WAREHOUSE
)

engine = create_engine(connString)

connection = engine.connect()

## SALES
## top product by country
result = engine.execute('\
    select country_code, country, product_ID, product, total_sales_units\
    from m_most_popular_product_by_country\
')
data = result.fetchall()
dfTopProductByCountry = pd.DataFrame(data).sort_values(by=['total_sales_units'])

figTopProductByCountry = px.bar(dfTopProductByCountry, x="product", y="total_sales_units", color="country", barmode="group")
figTopProductByCountry.layout.title = "Top seller products by country"

## popular products by country
result = engine.execute('\
    select country_code, country, product_ID, product, total_order_quantity\
    from m_popular_products\
')
data = result.fetchall()
dfPopularProducts = pd.DataFrame(data).sort_values(by=['total_order_quantity'], ascending=False)

figPopularProducts = px.bar(dfPopularProducts, x="country", y="total_order_quantity", color="product", barmode="group")
figPopularProducts.layout.title = "Product popularity in top sales country"

## USERS/TECHNICAL
## top product by country
result = engine.execute('\
    select user_agent, user_cnt\
    from m_popular_devices\
')
data = result.fetchall()
dfTopTechnicalAgentsUsed = pd.DataFrame(data).sort_values(by=['user_cnt'], ascending=False)

figTopTechnicalAgentsUsed = px.pie(dfTopTechnicalAgentsUsed, names="user_agent", values="user_cnt")
figTopTechnicalAgentsUsed.layout.title = "Client browser technical agents"
figTopTechnicalAgentsUsed.layout.autosize = False




app = Dash(__name__)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Customer DWH (Demo project)'),

    html.Div(children='''
        Operations dashboard (Dash)
    '''),

    dcc.Graph(
        id='example-graph',
        figure=figTopProductByCountry
    ),

    dcc.Graph(
        id='example-graph1',
        figure=figPopularProducts
    ),

    dcc.Graph(
        id='example-graph2',
        figure=figTopTechnicalAgentsUsed
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)