"""Email self whenever program finds a good deal"""


import os
import smtplib
import ssl
from dotenv import load_dotenv
import json
from data.colors_for_print import BAD, OK, GOOD, GREAT, END


def email_best_deals() -> None:
    """Function to call to email best deals"""

    analysis_json = _get_analyses_from_json()

    # If analysis_json is empty, there is no analyses
    if not analysis_json:
        print(f"{BAD}\n!!!   No email sent. Ending program...   !!!{END}")
        return

    print(f"{GOOD}\n!!!   Emailing best deals!   !!!{END}")

    best_deal, best_deals = _find_best_deals(analysis_json)
    message = _construct_message(analysis_json, best_deal, best_deals)
    _send_email(message)


def _get_analyses_from_json() -> dict:
    """Opens analysis.json and stores value in dict."""

    # Handle if file doesn't exist
    try:
        with open(os.path.join('output', 'analysis.json')) as json_file:
            analysis_json = json.load(json_file)
    except FileNotFoundError:
        analysis_json = {}

    return analysis_json


def _get_deal_value(analysis_json, deal) -> float:
    """Gets the value of a property"""

    return float(analysis_json[deal]['Analysis']['Cash on Cash Return'].lstrip('$').rstrip('%'))


def _find_best_deals(analysis_json) -> tuple:
    """Finds the best deal out of the analysis"""

    MINIMUM_ConC_PERCENT = 12
    best_deals = []

    # TODO Make this more complicated taking in max offer/price, all analysis other analysis. Multiple if statements
    # _get_deal_value() returns a tuple of all the meta analyses? Use for different if statements?
    for deal in analysis_json:
        if _get_deal_value(analysis_json, deal) > MINIMUM_ConC_PERCENT:
            best_deals.append(deal)

    best_deals.sort(key=lambda x: _get_deal_value(analysis_json, x), reverse=True)
    best_deal = best_deals[0]

    return best_deal, best_deals


def _construct_message(analysis_json, best_deal, best_deals) -> str:
    """Constructs the message with the subject line to email"""

    best_property = analysis_json[best_deal]

    # For each estimation in analysis, add an asterisk to subject line
    est = ''
    for _ in analysis_json[best_deal]['Estimations']:
        est += '*'

    subject_line = f"Subject: Real Estate Bot - " \
                   f"{_get_deal_value(analysis_json, best_deal)}%{est} ConC Return" \
                   f" @ ${best_property['Property Info']['Price ($)']:,}!"

    # Body of message filled according to find_best_deals()
    deals = "ORDERED FROM BEST TO WORST - THIS DOES NOT CONTAIN ALL THE PROPERTY ANALYSES, JUST THE BEST ONES:\n\n" \
            f"{'-'*196}\n"
    for deal in best_deals:

        info = analysis_json[deal]['Property Info']

        # 'https://' Doesn't get sent in email for some reason so slicing to zillow.
        deals += f"Property: {analysis_json[deal]['Property URL'][12:]}\n"

        deals += f'    Property Info: {{\n' \
                 f'        "Price": ${info["Price ($)"]:,}\n' \
                 f'        "Units": {info["Units"]:,}\n' \
                 f'        "Rent": ${info["Rent Per Unit ($)"]:,}\n}}\n'\
                 f'    Analysis: {json.dumps(analysis_json[deal]["Analysis"], indent=8)}\n' \
                 f'    Estimations: {json.dumps(analysis_json[deal]["Estimations"], indent=8)}\n' \
                 f'{"-"*196}\n'

    # Entire message with subject line and body to send
    message = f"{subject_line}\n\n" \
              f"{deals}"

    return message


def _send_email(message) -> None:
    """Sends the email with relevant analyses."""

    # Load credentials for email login from local environmental variable, .env file in main directory.
    load_dotenv()
    sender = os.getenv('REAL_ESTATE_CALCULATOR_BOT_EMAIL')
    password = os.getenv('REAL_ESTATE_CALCULATOR_BOT_PASSWORD')
    receiver = sender

    # Handles if .env file is missing
    if not sender or not password:
        print(f"\n{BAD}!!!   Error: No email or password found.  !!!{END}")
        print(f"{OK}This is likely due to missing .env file. "
              f"Follow instructions for emailing on github.{END}")
        return

    # Send email
    PORT = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

    print(f"\n{GREAT}!!!   Email successfully sent! Ending program...   !!!{END}")
