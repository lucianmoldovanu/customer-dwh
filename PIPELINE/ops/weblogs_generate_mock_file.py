import random
import datetime
import pandas as pd
import numpy as np

from dagster import op, Dict

@op
def generate_weblog_file(mockdata: Dict) -> None:
    acceptable_ip_prefixes = [i for i in range(1, 10)] + [i for i in range(11, 100)] + [i for i in range(101, 127)] + [i for i in range(128, 169)] + [i for i in range(173, 192)] + [i for i in range(199, 203)] + [i for i in range(204, 224)]

    customer_ids = [c[0] for c in mockdata['customers']]
    customer_id_to_ips = [(c, [f"{random.choice(acceptable_ip_prefixes)}.{random.randint(1, 255)}.100.{i+1}" for i in range(2)]) for c in customer_ids] #each customer has exactly 2 IDs from which he connects randomly

    START_TS = datetime.datetime(2021,10,20)
    
    #generate 10.000 stochastic time deltas (in milliseconds) between subsequent events (on a single timeline)
    time_deltas_millis = [random.randint(100000, 1000000) for i in range(20000)]

    df = pd.DataFrame(time_deltas_millis, columns=['tsdelta'])
    df['tscum'] = df['tsdelta'].cumsum()
    df['ts'] = START_TS + pd.TimedeltaIndex(df['tscum'] / 1000, unit='s')
    df['user_idx'] = df.apply(lambda r: random.randint(0, len(customer_id_to_ips)-1), axis=1)

    df['log'] = df.apply(lambda r: '%s %s %s %s %s %s %s %s %s' % (
        random.choice(customer_id_to_ips[r['user_idx']][1]),
        # '186.213.' + str(random.randint(1, 256)) + '.' + str(random.randint(1, 256)),
        '-',
        customer_ids[r['user_idx']],
        r['ts'],
        'GET / HTTP/1.0',
        '200',
        str(random.randint(1000, 15000)), #size kb
        '-',
        random.choice([
            'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        ])
    ), axis = 1)

    np.savetxt(r'PIPELINE/wlogs001.txt', df['log'], fmt = '%s')

# test support
if __name__ == "__main__":
    dummyObject = {}
    dummyObject['customers'] = [f"{c}" for c in range(0, 100)]
    run(dummyObject)