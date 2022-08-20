USE CDWH.CORE;

COPY INTO WLOGS FROM @%wlogs
    FILE_FORMAT = (FORMAT_NAME = 'fmt_weblogs', ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE)
    PATTERN = '.*wlogs001.txt.gz'
    ON_ERROR = 'skip_file';