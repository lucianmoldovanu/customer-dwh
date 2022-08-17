import subprocess, os

from dagster import op

from PIPELINE.utils import _sql_file_to_statements_array

@op(required_resource_keys={'snowflake'})
def refresh_b2b_data_model(context):
    for query in _sql_file_to_statements_array('PIPELINE/ops/b2b_create_datamodel.sql'):
        context.resources.snowflake.execute_query(query)

@op(required_resource_keys={'snowflake'})
def weblogs_setup(context, dummy) -> None:
    for query in _sql_file_to_statements_array('PIPELINE/ops/weblogs_setup.sql'):
        context.resources.snowflake.execute_query(query)

@op(required_resource_keys={'snowflake'})
def weblogs_load(context, dummy) -> None:
    for query in _sql_file_to_statements_array('PIPELINE/ops/weblogs_load.sql'):
        context.resources.snowflake.execute_query(query)

# DBT-dagster integration docs: https://docs.dagster.io/integrations/dbt
@op(required_resource_keys={"dbt"})
def run_dbt_all(context, dummy) -> None:
    context.resources.dbt.run() #models=["tag:staging"])

@op(required_resource_keys={"dbt"})
def run_dbt_test(context) -> None:
    context.resources.dbt.test() #models=["tag:staging"])