'''
Author: Jason
Creation Date: 19/02/2023

Run a basic flow with tasks

Note: A task is a function that represents a distinct piece of work executed within a flow. 

Referenced from:
https://docs.prefect.io/tutorials/first-steps/ 

'''
import requests
from prefect import flow, task

@task
def call_api(url):
    response = requests.get(url)
    print(response.status_code)
    return response.json()

@flow
def api_flow(url):
    fact_json = call_api(url)
    return fact_json

print(api_flow("https://catfact.ninja/fact"))
