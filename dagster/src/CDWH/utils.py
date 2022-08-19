import re
import random, time

def _sql_file_to_statements_array(fname):
    with open(fname, 'r') as file:
        s_queries = file.read()
        s_queries = re.sub('--(.*)\n','',s_queries + '\n').replace('\n', '') #remove comment lines and endlines
        s_queries = re.sub('\s+', ' ', s_queries) #remove multiple-spaces

    return [query.strip(' ') for query in s_queries.split(';')] #split into statements and trim whitespaces

def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end):
    prop = random.random()
    return str_time_prop(start, end, '%Y-%m-%d', prop)