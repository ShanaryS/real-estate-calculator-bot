from bs4 import BeautifulSoup
import requests

url = 'https://www.nerdwallet.com/mortgages/mortgage-rates'
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

table = doc.find('tbody')

interest_rates = []
for index, tr in enumerate(table.find_all('tr')):
    if index == 4 or index == 5 or index == 6:
        continue

    td = float(str(tr.find('td')).split('>')[-2].split('%')[0]) / 100
    interest_rates.append(td)

interest_rate_30_years = interest_rates[0]
interest_rate_20_years = interest_rates[1]
interest_rate_15_years = interest_rates[2]
interest_rate_10_years = interest_rates[3]
interest_rate_30_years_FHA = interest_rates[4]
interest_rate_30_years_VA = interest_rates[5]
