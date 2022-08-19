
<!-- docker run --rm -it \
    --network=host \
    -v $PWD/dbt/project/:/usr/app \
    -v $PWD/dbt/profiles.yml:/root/.dbt/profiles.yml \
    ghcr.io/dbt-labs/dbt-snowflake:latest -->

export SNOWFLAKE_HOST=fo97060.europe-west4.gcp SNOWFLAKE_USER=techexplorer1 SNOWFLAKE_PASS=????
docker-compose up --build --force-recreate