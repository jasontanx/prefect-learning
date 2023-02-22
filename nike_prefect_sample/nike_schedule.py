import requests
import re 
from bs4 import BeautifulSoup

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import IntervalSchedule
# from prefect.flow_runners import SubprocessFlowRunner [DEPRECATED]
from prefect.infrastructure import Process


# https://www.youtube.com/watch?v=XL4wgLUp-VA 
# https://medium.com/the-prefect-blog/deploy-prefect-pipelines-with-python-perfect-68c944a3a89f 
# https://www.youtube.com/watch?v=OjvkY7p0CYA 

'''
Prefect 2.0 changes
https://discourse.prefect.io/t/prefect-2-0b12-removes-flow-runners-in-favor-of-more-flexible-infrastructure-blocks/1232 
'''

@task(retries = 3) # 3 retries on this in case website error etc.
def find_price(url):
    '''
    find the price
    '''
    k = requests.get(url).text
    soup = BeautifulSoup(k, 'html.parser')
    price_string = soup.find('div', {"class": "product-price"}).text
    price_string = price_string.replace(' ', '')
    price = int(re.search('[0-9]+', price_string).group(0))
    return price

@task (cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def compare_price(price, budget):
    '''
    compare whether it is within our budget
    '''
    if price == budget:
        print(f"buy the shoe, it is a good deal.") 
    else:
        print(f"no, dont buy it now, it is:", price)

@flow
def nike_flow(url, budget):
    '''
    call previous 2 functions
    '''
    price = find_price(url)
    compare_price(price, budget)


deployment = Deployment.build_from_flow(
    flow=nike_flow,
    name="Nike Shoe Flow",
    schedule=IntervalSchedule(interval=timedelta(minutes=10)), # every 10 minutes run
    parameters={"url": "https://www.nike.com/my/t/air-force-1-07-shoe-NMmm1B/DD8959-100", "budget": 300},
    tags=["Experiment-1"],
    infrastructure=Process() # could be replaced by kubernetes, docker etc.
)

if __name__ == "__main__":
    deployment.apply()
