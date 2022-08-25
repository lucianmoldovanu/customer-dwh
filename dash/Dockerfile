FROM python:3.10-slim

RUN apt-get update && apt-get upgrade --assume-yes && apt-get --assume-yes install  curl unzip

WORKDIR /usr/src/app

# Take environment variables at build and set into container
ARG ARG_SNOWFLAKE_HOST
ARG ARG_SNOWFLAKE_USER
ARG ARG_SNOWFLAKE_PASS

ENV SNOWFLAKE_HOST $ARG_SNOWFLAKE_HOST
ENV SNOWFLAKE_USER $ARG_SNOWFLAKE_USER
ENV SNOWFLAKE_PASS $ARG_SNOWFLAKE_PASS

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src ./

# CMD python -b 0.0.0.0:80 app.app:server