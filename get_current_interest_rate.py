from bs4 import BeautifulSoup
import requests

url = "https://www.nerdwallet.com/mortgages/mortgage-rates"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

table = doc.find("tbody")
interest_rate_30_years = float(str(table.td).split('>')[-2].split('%')[0]) / 100
interest_rate_20_years = 0.04
interest_rate_15_years = 0.04
interest_rate_10_years = 0.04
interest_rate_30_years_FHA = 0.04
interest_rate_30_years_VA = 0.04
