"""Email self whenever program finds a good deal"""


import os
import smtplib
import ssl
from dotenv import load_dotenv


load_dotenv()
sender = os.getenv('REAL_ESTATE_CALCULATOR_BOT_EMAIL')
password = os.getenv('REAL_ESTATE_CALCULATOR_BOT_PASSWORD')
receiver = sender

message = """\
Subject: Test Email # 2

This is from a script!

Best,
Shanary
"""

PORT = 465
context = ssl.create_default_context()

print('Sending email')
with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
print('Sent email')
