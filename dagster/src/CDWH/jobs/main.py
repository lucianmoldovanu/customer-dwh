from dagster import job
from dagster_snowflake import snowflake_resource
from dagster_dbt import dbt_cli_resource

import CDWH.ops.main as ops
from CDWH.ops.refresh_mock_data import refresh_mock
from CDWH.ops.weblogs_generate_mock_file import generate_weblog_file
from CDWH.ops.weblogs_transfer import transfer_weblogs

@job(resource_defs={'snowflake': snowflake_resource, 'dbt': dbt_cli_resource})
def build_datamodel_populate_mock():
    a = ops.refresh_b2b_data_model()
    mockdata = refresh_mock(a)

    ws_setup = ops.weblogs_setup(a)
    ws_gen = generate_weblog_file(mockdata)
    ws_trans = transfer_weblogs(ws_gen, ws_setup)
    ws_load = ops.weblogs_load(ws_trans)

    ops.run_dbt_all(ws_load)

# testing
if __name__ == "__main__":
    build_datamodel_populate_mock()