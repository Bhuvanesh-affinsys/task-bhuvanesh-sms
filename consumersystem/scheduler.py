import sys
import schedule
import requests
import os


def initiatePush():
    requests.get("http://127.0.0.1:8000/balance/")


schedule.every().friday.do(initiatePush)
