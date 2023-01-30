import argparse
from time import time
import os
import pandas as pd
from sqlalchemy import create_engine


def main(args):
    user = args.user
    password = args.password
    hostname = args.host
    port = args.port
    dbname = args.dbname
    tablename = args.tablename
    url = args.url

    # download the csv
    file_name = 'output.csv.gz'
    csv_name = 'output.csv'
    os.system(f"wget {url} -O {file_name}")
    os.system(f"gzip -d {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{hostname}:{port}/{dbname}')

    df = pd.read_csv(csv_name, nrows=1)
    # NOTE: Yellow taxi table uses tpep / Green lpep
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(0).to_sql(name=tablename, con=engine, if_exists='replace')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    for chunk in df_iter:
        t_start = time()
        chunk.lpep_pickup_datetime = pd.to_datetime(chunk.lpep_pickup_datetime)
        chunk.lpep_dropoff_datetime = pd.to_datetime(chunk.lpep_dropoff_datetime)
        chunk.to_sql(name=tablename, con=engine, if_exists='append')
        t_end = time()
        print(f'Inserted another chunk ({t_end - t_start:.3f} seconds)')

    os.system(f"wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv")
    df_zones = pd.read_csv("taxi+_zone_lookup.csv")
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # user, password, host, port, database name, table name, url of the csv
    parser.add_argument('--user', help='user name for postgres', type=str)
    parser.add_argument('--password', help='user name for postgres', type=str)
    parser.add_argument('--host', help='host name to connect to postgres', type=str)
    parser.add_argument('--port', help='port to connect to postgres', type=int)
    parser.add_argument('--dbname', help='database name for postgres', type=str)
    parser.add_argument('--tablename', help='table name for postgres', type=str)
    parser.add_argument('--url', help='url of the csv', type=str)

    args = parser.parse_args()

    main(args)
