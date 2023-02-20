'''
Author: Jason

'''

import yfinance as yf
from datetime import timedelta
from datetime import datetime
from prefect import flow, task


@task(retries=3, cache_expiration=timedelta(30))
def fetch_data(ticker):
    return yf.download(ticker)


@task
def save_data(stock_df):
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"

    stock_df.to_csv(file_name)
    # stock_df.to_csv()


@flow
def pipeline(ticker):
    df = fetch_data(ticker)
    print(df.head())
    save_data(df)


if __name__ == "__main__":
    pipeline("AAPL")
