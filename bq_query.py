from prefect import flow
from prefect_gcp import GcpCredentials
from prefect_gcp.bigquery import bigquery_query
# from cred import GcpCredentials

import pandas as pd

'''
# creating blocks --> prefect GCP
https://prefecthq.github.io/prefect-gcp/
https://prefecthq.github.io/prefect-gcp/credentials/#prefect_gcp.credentials.GcpCredentials  
https://prefecthq.github.io/prefect-gcp/bigquery/#prefect_gcp.bigquery.bigquery_query 

# youtube
https://www.youtube.com/watch?v=AI-Ks5x7Mp4 

# gcp BQ query
https://www.prefect.io/guide/blog/get-integrated-to-google-cloud-platform-with-prefect-gcp/ 

# notifications (extra)
https://www.youtube.com/watch?v=PC1PgBB438Y 

'''

# query = "SELECT * FROM `myfirstproject-364809.socio_demographic.salaries_ethnicity_sex` WHERE year = '2021' LIMIT 10"

gcp_credentials_block = GcpCredentials.load("gcp-project-1")

@flow
def bigquery_query_flow(
    location: str = "asia-southeast1"):
    # gcp_credentials = GcpCredentials()  # inferred from env, or set service_account_file
    query = "SELECT * FROM `myfirstproject-364809.socio_demographic.salaries_ethnicity_sex` WHERE year = '2021' LIMIT 10"
    result = bigquery_query(query, gcp_credentials_block, location=location)
    # result.to_dataframe()
    df = pd.DataFrame(result)
    print(df)
    df.to_csv('sample1.csv')

bigquery_query_flow()
