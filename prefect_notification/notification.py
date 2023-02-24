'''
reference:
https://www.youtube.com/watch?v=PC1PgBB438Y 
https://api.slack.com/messaging/webhooks 


'''

from prefect import task, flow
from prefect.blocks.notifications import SlackWebhook # import webhook module


@task(name="Slacknotif")
def test_notif(name="slacknoti"):
    slack_webhook_block = SlackWebhook.load("testslackblock") # load slackwebhook block
    slack_webhook_block.notify("Hello from Prefect!") # create notification

@flow(name="Important-2.0-Flow")
def basic_flow():
    test_notif()


basic_flow()
