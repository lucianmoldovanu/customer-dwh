import subprocess, os
from dagster import op

@op
def transfer_weblogs(context, dummy1, dummy2) -> None:
    file_path = 'file://' + os.getcwd() + '/PIPELINE/wlogs001.txt @CUSTOMER_DWH.B2B.%wlogs'
    res = subprocess.run([
        "snowsql",
        '-c',
        'CUSTOMER_DWH_PROFILE',
        '-q',
        'put ' + file_path,
        # '-o', #if enabled, will generate 2 detailed log files in the root folder
        # 'log_level=DEBUG'
    ], capture_output=True, text=True)

    if res.stderr or "File doesn't exist" in res.stdout:
        raise BaseException(f"Cannot upload local file to Snowflake! File is not existing: {file_path}")