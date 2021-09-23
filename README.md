# Real Estate Calculator Bot

Work in progress... A bot for analyzing real estate properties. Currently fully functional for analyzing deals if given a https://www.zillow.com/homedetails/* url. Gets property data from zillow and property taxes from https://www.countyoffice.org/tax-records/ if not on zillow. Mortgage interest rates scraped from https://www.nerdwallet.com/mortgages/mortgage-rates.

Returns color coded information in terminal such as Return on Investment, Cash on Cash Return, Caprate, Cashflow, Maximum Suggested Offer, and recommended emergency fund.

(Over fitted to multi-family properties in CT. To fix: edit CONSTANTS found in user.py to fit your heuristics. CONSTANTS are all caps like that.)
