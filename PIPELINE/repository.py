from dagster import repository

from PIPELINE.jobs.main import build_datamodel_populate_mock
from PIPELINE.jobs.test import test_dbt
from PIPELINE.jobs.ip_to_countries import refresh_ip_to_countries

@repository
def PIEPLINE():
    """
    The repository definition for this Dagster repository.

    For hints on building your Dagster repository, see our documentation overview on Repositories:
    https://docs.dagster.io/overview/repositories-workspaces/repositories
    """
    jobs = [build_datamodel_populate_mock, refresh_ip_to_countries, test_dbt]
    # schedules = [my_hourly_schedule]
    # sensors = [my_sensor]

    return jobs #+ schedules + sensors
