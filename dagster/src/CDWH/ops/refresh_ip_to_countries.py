#!/usr/bin/env python3
import os
from dagster import op
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json

# arguments
SNOWFLAKE_DB = 'CDWH'
SNOWFLAKE_SCHEMA = 'CORE'
SNOWFLAKE_WAREHOUSE = 'CDWH_WH'

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class IpCountryCache(Base):
    __tablename__ = "ip_country_cache"
    ip = Column(String(15), primary_key=True)
    country_code = Column(String(3))
    country = Column(String(255))
    message = Column(String(255))

@op
def refresh_in_batches():
    connString = 'snowflake://{user}:{password}@{account_identifier}/{db}/{schema}?warehouse={warehouse}'.format(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASS'],
        account_identifier=os.environ['SNOWFLAKE_HOST'],
        db=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )

    engine = create_engine(connString)

    connection = engine.connect()
    engine.execute("delete from ip_country_cache where timestampdiff('day', DATE_REFRESHED, current_timestamp) >= 5")
    
    while True:
        result = engine.execute('select top 100 log.ip from stg_weblogs log left join ip_country_cache cache on log.ip = cache.ip where cache.ip is null group by log.ip')
        rows = result.fetchall()

        if(len(rows) == 0):
            break #premature termination - no more results to process

        ip_adresses = [r[0] for r in rows]

        data = [dict(zip(['query', 'lang'], [ip, "en"])) for ip in ip_adresses]
        res = requests.post("http://ip-api.com/batch", json.dumps(data))
        
        res_proc = [(r['query'], r['countryCode'], r['country'], None) if r['status'] != 'fail' else (r['query'], None, None, r['message']) for r in res.json()]
        print(res_proc)

        DBSession = scoped_session(sessionmaker())
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)

        DBSession.bulk_save_objects(
            [
                IpCountryCache(ip = r[0], country_code = r[1], country = r[2], message = r[3]) for r in res_proc
            ]
        )

        DBSession.commit()

        engine.execute('\
            update stg_weblogs log\
            set country_code = cache.country_code\
            from ip_country_cache cache\
            where log.ip = cache.ip and log.country_code is null and cache.ip is not null\
        ')

    connection.close()
    engine.dispose()