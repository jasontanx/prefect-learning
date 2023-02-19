'''
Author: Jason
Creation Date: 19/02/2023

Theme: Run flows with parameters

Referenced from:
https://docs.prefect.io/tutorials/first-steps/ 

'''

import requests
from prefect import flow

@flow
def call_api(url):
    return requests.get(url).json()

api_result = call_api("http://time.jsontest.com/")
print(api_result)
