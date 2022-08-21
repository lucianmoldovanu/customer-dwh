FROM python:3.10-slim

RUN apt-get update && apt-get upgrade --assume-yes && apt-get --assume-yes install  curl unzip

# Change working directory
WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

ARG ARG_SNOWFLAKE_HOST
ARG ARG_SNOWFLAKE_USER
ARG ARG_SNOWFLAKE_PASS

#TODO: run with non-sql user, see https://github.com/kurron/docker-snowsql/blob/master/Dockerfile

# setup snowsql defaults such that setup can be automated
ENV SNOWSQL_DEST /usr/local/bin 
ENV SNOWSQL_LOGIN_SHELL /root/.bashrc
# ENV SNOWSQL_PWD $ARG_SNOWFLAKE_PASS

# install SNOWSQL
RUN curl -o snowsql-1.2.22-linux_x86_64.bash https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.22-linux_x86_64.bash
RUN bash snowsql-1.2.22-linux_x86_64.bash
RUN snowsql -v

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV SNOWFLAKE_HOST $ARG_SNOWFLAKE_HOST
ENV SNOWFLAKE_USER $ARG_SNOWFLAKE_USER
ENV SNOWFLAKE_PASS $ARG_SNOWFLAKE_PASS

# RUN ECHO "luc\n $ARG_SNOWFLAKE_HOST ${SNOFLAKE_HOST} ${ARG_SNOWFLAKE_HOST}"
RUN mkdir /root/.dbt

RUN echo "\
DBT_PROFILE_CDWH_SNOWFLAKE:\n\
  outputs:\n\
    dev:\n\
      type: snowflake\n\
      threads: 1\n\
      account: $ARG_SNOWFLAKE_HOST\n\
      database: CDWH\n\
      schema: CORE\n\
      warehouse: CDWH_WH\n\
      user: $ARG_SNOWFLAKE_USER\n\
      password: $ARG_SNOWFLAKE_PASS\n\
      role: ACCOUNTADMIN\n\
  target: dev\
" >> /root/.dbt/profiles.yml

# Copy source code
# COPY ./dagster.yaml .
COPY  ./src .

RUN echo "\
[connections.SNOWSQL_CDWH_PROFILE]\n\
accountname = $ARG_SNOWFLAKE_HOST\n\
username = $ARG_SNOWFLAKE_USER\n\
password = $ARG_SNOWFLAKE_PASS\n\
dbname = CDWH\n\
schemaname = CORE\n\
warehousename = CDWH_WH\
" >> /root/.snowsql/config

CMD ["dagit", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]