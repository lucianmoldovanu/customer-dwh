FROM python:3.10-slim

# Change working directory
WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /dbt

ARG ARG_SNOWFLAKE_HOST
ARG ARG_SNOWFLAKE_USER
ARG ARG_SNOWFLAKE_PASS

ENV SNOWFLAKE_HOST $ARG_SNOWFLAKE_HOST
ENV SNOWFLAKE_USER $ARG_SNOWFLAKE_USER
ENV SNOWFLAKE_PASS $ARG_SNOWFLAKE_PASS

# RUN ECHO "luc\n $ARG_SNOWFLAKE_HOST ${SNOFLAKE_HOST} ${ARG_SNOWFLAKE_HOST}"
RUN echo "\
DBT_PROFILE_CDWH_SNOWFLAKE:\n\
  outputs:\n\
    dev:\n\
      type: snowflake\n\
      threads: 1\n\
      account: $ARG_SNOWFLAKE_HOST\n\
      database: DB_CDWH\n\
      schema: SCH_CDWH\n\
      warehouse: WH_CDWH\n\
      user: $ARG_SNOWFLAKE_USER\n\
      password: $ARG_SNOWFLAKE_PASS\n\
      role: ACCOUNTADMIN\n\
  target: dev\
" >> /dbt/profiles.yml

# Copy source code
# COPY ./dagster.yaml .
COPY  ./src .

CMD ["dagit", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]