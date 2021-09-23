"""Email self whenever program finds a good deal"""


import os
import smtplib
import ssl
from dotenv import load_dotenv
import json


# Load credentials for email login from local environmental variable
load_dotenv()
sender = os.getenv('REAL_ESTATE_CALCULATOR_BOT_EMAIL')
password = os.getenv('REAL_ESTATE_CALCULATOR_BOT_PASSWORD')
receiver = sender


# Property analysis that will be sent in the email body
with open(os.path.join('output', 'analysis.json')) as json_file:
    analysis_json = json.load(json_file)
deals = analysis_json

# Email subject and body
message = f"""\
Subject: Property Analyses Results!

{deals}

"""

# Sending email
PORT = 465
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
