import urllib.request
import os

def lambda_handler(event, context):
    response = urllib.request.Request("https://smsjournal.xyz/journals/api_daily_metrics/",
                                              data={"api_key": os.environ["api_key"]},
                                              method="POST")
