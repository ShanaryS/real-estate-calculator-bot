# Real Estate Calculator Bot

## Features

* Automatically send an email whenever a great investment oppurtunity arises, according to your heuristics.
* Analayze a property given a https://www.zillow.com/homedetails/* URL. Print to output or store locally in JSON.
* Get property URLs from a search a zillow search page to automatically analyze all properties of a criteria (Solves captcha if it appears).
* Easy adding, deleting, ignoring, and overwriting saved URLs with a decesion tree.
* Uses real time interest rates

## Examples

<p align="center">
  <strong>Instantly analyze a single property with all the gory details!</strong>
</p>

<p align="center">
  Shows popular analytic metries for analyzing a real estate property as well as the amortization table of the loan:
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134757381-ec233d45-3133-41a1-915b-cc3090dde7f4.gif" alt="animated" />
</p>

## About

This is a bot for analyzing real estate properties. Able to either analyze a single property and print its analysis or input a search criteria that analyze all the properties that fit. Emails best deals from all the properties analyzed. Analysis includes: 
```
Return On Investment, Cash on Cash Return, Caprate, Cashflow, Max Offer, Emergency Fund, Amortizaton Table*
```
###### * When printing analysis of a single property only.

Data is stored locally in JSON files in /output/ as well as the logs for errors. The URLs inputted (from run_property_tracker) are saved in urls.json while the final analysis of all those URLs are stored in analysis.json. The [README.md](https://github.com/ShanaryS/algorithm-visualizer/blob/main/LICENSE) in /output/ contains more information on how data and errrors are stored.

Requires either a https://www.zillow.com/homedetails/* URL for individual properties or a search URL. Adding, deleting, and ignoring properties are done through a decesion tree in the terminal. It contains the necessary information on how to use each option.

Interest rates are retrieved once at start up from https://www.nerdwallet.com/mortgages/mortgage-rates and used for all subsquent analysis in the session. Property taxes are retrieved from the Zillow property page if it exists, else it defaults to https://www.countyoffice.org/tax-records/ which usually has the info. (Note: There is a limit on the number times you can get the property taxes info from the county office, at 5 properties, you will be restricted for the day. Luckily Zillow usually has the property taxes and thus rarely falls back to county office. Though if you wanted to get around that limitation, you would need to use a VPN.

The resutling analyses is currently over fitted to multi-family properties in CT. To fix, edit the CONSTANTS found in values.py to fit your heuristics. CONSTANTS are defined by all caps. In there you can also adjust the critria for a 'good deal' which decides what properties to email.

## Installation

Clone this repo and cd into it:

```bash
git clone https://github.com/ShanaryS/real-estate-calculator-bot.git
cd real-estate-calculator-bot
```

Create and activate your virtual environment:

* Windows:
```bash
virtualenv env
.\env\Scripts\activate
```

* MacOS/Linux:
```bash
virtualenv --no-site-packages env
source env/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

# Usage

#### All the files that you should interact with to use the program is in the main directory. Either prefixed with run_* or values.py for editing constants.

* Add a property or search critria to track:
```bash
python run_property_tracker
```

* Analyze all tracked properties:
```bash
python run_analysis
```

* Refresh search properties without input (Useful for automatically refreshing unattended):
```bash
python run_refresh_listings_from_search
```

* Print analysis of single property without saving, including amortizaiton table (Useful for just analyzing a single property):
```bash
python run_single_property_analysis_print_only
```

## License
[MIT](https://github.com/ShanaryS/algorithm-visualizer/blob/main/LICENSE)
