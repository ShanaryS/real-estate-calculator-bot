# Real Estate Calculator Bot

Work in progress... A webscraper for anlyzing real estate properties. Currently fully functional for analyzing deals if given an https://www.zillow.com/homedetails/* url. Gets property data from zillow and property taxes from https://www.countyoffice.org/tax-records/ if not on zillow. Mortage interest rates scraped from https://www.nerdwallet.com/mortgages/mortgage-rates.

Returns color coded information in terminal such as Return on Investment, Cash on Cash Return, Caprate, Cashflow, Maximum Suggested Offer, and recomended emergency fund.

(Overfitted to multi-family properties in CT. To fix: user.RENT_PER_UNIT, a default value, would need to double or even triple for some areas.)
