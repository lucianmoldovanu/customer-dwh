import subprocess, os
from dagster import op

@op
def transfer_weblogs(wlog_generated, wlog_setup) -> str:
    file_path = 'file://' + os.getcwd() + '/' + wlog_generated
    res = subprocess.run([
        "snowsql",
        '-c',
        'SNOWSQL_CDWH_PROFILE',
        # '-a',
        # '$SNOWFLAKE_HOST',
        # '-u',
        # '$SNOWFLAKE_USER',
        # '-d',
        # 'CDWH',
        # '-s',
        # 'CORE',
        # '-w',
        # 'CDWH_WH',
        '-q',
        'put ' + file_path + ' @%WLOGS',
        '-o', #if enabled, will generate 2 detailed log files in the root folder
        'log_level=DEBUG'
    ], capture_output=True, text=True)

    if res.stderr or "File doesn't exist" in res.stdout:
        raise BaseException(f"Cannot upload local file OR generic Snowflake error: {res.stderr}")

    return 'done'

# testing
if __name__ == "__main__":
    transfer_weblogs('CDWH/wlogs001.txt', None)