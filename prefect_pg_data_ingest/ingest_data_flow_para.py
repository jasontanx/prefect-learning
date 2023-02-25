
# Creation Date: 7/2/2023 (D/M/YYYY)
# Topic: DE Zoomcamp 2.2.2 - Introduction to Prefect Concepts
# Code Referenced from:
# ETL 
# Padilha -> https://github.com/padilha/de-zoomcamp/blob/master/week1/ingest_data.py
# https://www.youtube.com/watch?v=cdtN6dhp708&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19
# Succesful run in local (mac)

import pandas as pd
import argparse
import os
from sqlalchemy import create_engine
from time import time

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# created two new task (ETL)
# 1. extract data [NEW]
# 2. transform data [NEW]
# 3. ingest data

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    if url.endswith('csv.gz'):
        csv_name = 'yellow_tripdata_2021-01.csv.gz'
    else:
        csv_name = 'output.csv'
    
    os.system(f"wget {url} -O {csv_name}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000) # create dataframe

    df = next(df_iter)
    # change date columns from string to datetime format
    df.tpep_pickup_datetime = pd.to_datetime(df['tpep_pickup_datetime'])
    df.tpep_dropoff_datetime = pd.to_datetime(df['tpep_dropoff_datetime'])
    return df


@task(log_prints=True)
def transform_data(df):
    print(f"pre:missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passeger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3) # able to receive metadata about upstearm dependencies
def ingest_data(user, password, host, port, db, table_name, df):
    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(postgres_url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

@flow(name="SubFlow", log_prints=True)
def log_subflow(table_name:str):
    print("Logging Subflow for: {table_name}")


@flow(name='Ingest Flow') # added @ flow and a new function 
def main_flow(table_name: str):
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    table_name = table_name
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(table_name)
    raw_data = extract_data(csv_url)
    data = transform_data(raw_data)
    ingest_data(user, password, host, port, db, table_name, data)


if __name__ == '__main__':
    main_flow("yellow_taxi_trips")
