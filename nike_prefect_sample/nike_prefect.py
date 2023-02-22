import requests
import re 
from bs4 import BeautifulSoup

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

# https://www.youtube.com/watch?v=XL4wgLUp-VA 

@task(retries = 3) # 3 retries on this in case website error etc.
def find_price(url):
    '''
    find the price
    '''
    k = requests.get(url).text
    soup = BeautifulSoup(k, 'html.parser') # create error by typing 'html.parser' as 'htmml.parser'
    price_string = soup.find('div', {"class": "product-price"}).text
    price_string = price_string.replace(' ', '')
    price = int(re.search('[0-9]+', price_string).group(0))
    return price

@task (cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
# caching -- if same inputs coming, dont need to run everything
# will hash the input and compare with previous succeeding
def compare_price(price, budget):
    '''
    compare whether it is within our budget
    '''
    if price <= budget:
        print(f"buy the shoe, it is a good deal.", price) 
    else:
        print(f"no, dont buy it now, it is:", price)

@flow
def nike_flow(url, budget):
    '''
    call previous 2 functions
    '''
    price = find_price(url)
    compare_price(price, budget)


url = 'https://www.nike.com/my/t/air-force-1-07-shoe-NMmm1B/DD8959-100'
#budget = 300
budget = 450
nike_flow(url, budget)

# using both task inside a flow - more observability
