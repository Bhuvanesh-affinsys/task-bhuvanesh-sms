import os
from dotenv import load_dotenv
import smtplib


from twilio.rest import Client

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
USE_TWLIO = os.getenv("USE_TWILIO") == "TRUE"
USE_EMAIL = os.getenv("USE_EMAIL") == "TRUE"
client = Client(ACCOUNT_SID, AUTH_TOKEN)


def sendSMS(to, body):
    if USE_TWLIO:
        message = client.messages.create(to="+91" + to, from_=TWILIO_NUMBER, body=body)
        return message
    else:
        print(f"{to}   {body}   ")


def sendMail(to, body):
    smtpclient = smtplib.SMTP("smtp.gmail.com", 587)
    smtpclient.starttls()
    smtpclient.login("bhuvanesh.e@affinsys.com", GOOGLE_APP_PASSWORD)
    smtpclient.sendmail("bhuvanesh.e@affinsys.com", to, body)
    smtpclient.quit()
