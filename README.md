# Real Estate Calculator Bot

## Features

* Parses the HTML doc of a zillow property page or search page using BeautifulSoup, Selenium, and RegEx. Defeating captchas along the way.
* Automatically send an email via SMPT with SSL whenever a great investment opportunity arises, according to your heuristics.
* Email credentials can be saved in a .env file for a temporary creation of an environmental variable.
* Analyze a property given a https://www.zillow.com/homedetails/* URL. Print analysis or store locally in JSON.
* Get property URLs from a search a zillow search page to automatically analyze all properties of a criteria (Solves captcha if it appears).
* Easy adding, deleting, ignoring, and overwriting saved URLs with a decision tree.
* Uses real time mortgage interest rates.
* Errors are gracefully handled and saved in a log file which includes exception type, traceback, and offers potential solutions to the issue. Failures do not interrupt the program, that specific property is simply skipped in the analysis.
* Inputs are checked to prevent errors as well as URLs are verified to be valid.
* Uses hash maps and set operations for quick calculations and manipulations of data.

## Examples

<p align="center">
  <strong>Instantly analyze a single property with all the fundamental real estate metrics!</strong>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134757381-ec233d45-3133-41a1-915b-cc3090dde7f4.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Automatically get property URLs from a search criteria! (P.S. Also beats captchas!)</strong>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134758448-b0ae8310-2c15-44dc-a823-7d1013786cba.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Analyze thousands of properties faster than you ever could!</strong>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134757517-5fcf1d08-4d63-41d9-9154-16a06bb4d24a.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Adding new properties to track is easy with the decision tree!</strong>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134757474-989d118e-c455-4e96-80aa-a2a810fcdf9b.gif" alt="animated" />
</p>

***

<p align="center">
  <strong>Automatically get emailed whenever the best deals are found!</strong>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/86130442/134757809-bf3e8926-ba67-472a-9db8-b34de1509bc0.png" />
  <img src="https://user-images.githubusercontent.com/86130442/134757813-a916fb12-ea08-4c93-8802-f649863775fd.png" />
</p>

## About

This is a bot for analyzing residential (1-4 units) real estate properties. Able to either analyze a single property and print its analysis or input a search criteria that analyze all the properties that fit. Emails best deals from all the properties analyzed. Analysis includes: 
```
Return On Investment, Cash on Cash Return, Caprate, Cashflow, Max Offer, Emergency Fund, Amortizaton Table*
```
###### * When printing analysis of a single property only.

Data is stored locally in JSON files in /output/ as well as the logs for errors. The URLs inputted (from run_property_tracker) are saved in urls.json while the final analysis of all those URLs are stored in analysis.json. The [README.md](https://github.com/ShanaryS/algorithm-visualizer/blob/main/LICENSE) in /output/ contains more information on how data and errors are stored.

Requires either a https://www.zillow.com/homedetails/* URL for individual properties or a search URL. Adding, deleting, and ignoring properties are done through a decision tree in the terminal. It contains the necessary information on how to use each option.

Interest rates are retrieved once at start up from https://www.nerdwallet.com/mortgages/mortgage-rates and used for all subsequent analysis in the session. Property taxes are retrieved from the Zillow property page if it exists, else it defaults to https://www.countyoffice.org/tax-records/ which usually has the info. (Note: There is a limit on the number times you can get the property taxes info from the county office, at 5 properties, you will be restricted for the day. Luckily Zillow usually has the property taxes and thus rarely falls back to county office. Though if you wanted to get around that limitation, you would need to use a VPN.)

The resulting analyses is currently over fitted to multi-family properties in CT. To fix, edit the CONSTANTS found in values.py to fit your heuristics. CONSTANTS are defined by all caps. In there you can also adjust the criteria for a 'good deal' which decides what properties to email.


## Notes

* To get the property URLs from a search URL, selenium is required (For direct property analysis, either through print or run_analysis, it is not required). The properties are dynamically loaded behind a JavaScript script. The only way of accessing those properties is to scroll to the bottom of the page, then parse the html doc. I am using the [chromedriver](https://chromedriver.chromium.org/downloads) for selenium. Tutorial for setting up [here](https://sites.google.com/chromium.org/driver/getting-started?authuser=0).
* Emails are sent over the gmail SMTP server. It is not necessary to the program, but a nice bonus. For using the email feature, I recommend using a separate gmail account to send/receive the mail. Enable 2FA and use an app password for the script. I suggest creating a local ".env" file in the parent directory containing two lines of your email and app password. More details are in push_best_deals_to_email.py.
* To automate this program, I recommend using Windows task scheduler or the Mac/Linux equivalent. There was no need to have this program running 24/7.

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

* Add a property or search criteria to track:
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

* Print analysis of single property without saving, including amortization table (Useful for just analyzing a single property):
```bash
python run_single_property_analysis_print_only
```

## License
[MIT](https://github.com/ShanaryS/algorithm-visualizer/blob/main/LICENSE)
