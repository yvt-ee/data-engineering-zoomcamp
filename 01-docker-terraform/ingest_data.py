#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import gzip

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    file_path = params.file_path  # Changed from 'url' to 'file_path'
    # url = params.url

    # Verify the local file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # USE URL
    # if url.endswith('.csv.gz'):
    #     csv_name = 'output.csv.gz'
    # else:
    #     csv_name = 'output.csv'

    # os.system(f"wget {url} -O {csv_name}")

    # download the csv

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')


    # Read CSV in chunks
    df_iter = pd.read_csv(file_path, iterator=True, chunksize=100000)

    # df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    # Assuming df_iter is already initialized and engine is your SQLAlchemy engine
    while True:
        try:
            t_start = time()
            df = next(df_iter)  # Get the next chunk of data

            # # Convert datetime columns to datetime type
            # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # Insert the chunk into the database
            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()
            print(f'Inserted another chunk..., took {t_end - t_start:.3f} seconds')

        except StopIteration:
            print("All chunks have been processed.")
            break  # Exit the loop when no more chunks are available

        except Exception as e:
            print(f"Error occurred: {e}")
            break  # Optionally, you can break on error or handle it differently


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we write the results to')
    parser.add_argument('--file_path', required=True, help='local path of the CSV file')  # Changed argument name to file_path
    # parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args() 
    main(args)