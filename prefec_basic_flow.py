'''
Author: Jason
Creation Date: 19/02/2023

Theme: Run a basic flow

Referenced from: 
https://docs.prefect.io/tutorials/first-steps/ 

'''

from prefect import flow, task

@task
def say_hello():
	print("Hello, World! I'm Marvin!")


@flow(name = "Prefect 2.0 Flow")
def marvin_flow():
	say_hello()


marvin_flow() # "Hello, World! I'm Marvin!"
