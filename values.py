"""DEFAULT VALUES USED FOR ANALYSIS. CHANGE THESE VALUES ACCORDING TO YOUR HEURISTICS. TOUCH NOTHING ELSE."""

'''If you want to change the criteria for a 'good deal' that it emails, that would be changed in
/web/push_best_deals_to_email.py with the functions _get_deal_value() and _find_best_deals().
Currently it just emails any property with a Cash On Cash Return greater than 12%. That is universally considered
a 'good deal'. You may increase or decrease the percentage by changing MINIMUM_ConC_PERCENT from 12. Different areas
may have too many deals above 12% or too little.
'''

# This value is used as the cut off for a good deal. Increasing or lowering it will change the minimum cutoff for
# a property to be sent within the email. Default value of 12. 12% ConC is universally considered good.
MINIMUM_ConC_PERCENT = 12

# Default values assumed if not found. Backup below.
DOWN_PAYMENT_PERCENT = 0.20
YEARS = 30  # 'FHA' and 'VA' requires YEARS = 30. 'Conventional' has options for YEARS = 30, 20, 15, 10.
LOAN_TYPE = 'Conventional'  # Options are 'Conventional', 'FHA', 'VA'. !!! NOTE: 'FHA' and 'VA' requires YEARS = 30.
PROPERTY_TAXES = 4000
FIX_UP_COST = 10000
CLOSING_PERCENT = 0.03
NUM_UNITS = 2
RENT_PER_UNIT_SINGLE = 1000
RENT_PER_UNIT_DUPLEX = 800
RENT_PER_UNIT_TRIPLEX = 650
RENT_PER_UNIT_QUADRUPLEX = 575
VACANCY_PERCENT = 0.08
MAINTENANCE_PERCENT = 0.15
MANAGEMENT_PERCENT = 0.10
DEPRECIATION_SHORT_PERCENT = 0.08
DEPRECIATION_LONG_PERCENT = 0.75
TAX_BRACKET = 0.24
IS_FIRST_RENTAL = True  # If 'False', halves emergency fund recommendation.


'''ORIGINAL VALUES TO RESET TO'''
# DOWN_PAYMENT_PERCENT = 0.20
# YEARS = 30  # 'FHA' and 'VA' requires YEARS = 30. 'Conventional' has options for YEARS = 30, 20, 15, 10.
# LOAN_TYPE = 'Conventional'  # Options are 'Conventional', 'FHA', 'VA'. !!! NOTE: 'FHA' and 'VA' requires YEARS = 30.
# PROPERTY_TAXES = 4000
# FIX_UP_COST = 10000
# CLOSING_PERCENT = 0.03
# NUM_UNITS = 3
# RENT_PER_UNIT_SINGLE = 1000
# RENT_PER_UNIT_DUPLEX = 800
# RENT_PER_UNIT_TRIPLEX = 650
# RENT_PER_UNIT_QUADRUPLEX = 575
# VACANCY_PERCENT = 0.08
# MAINTENANCE_PERCENT = 0.15
# MANAGEMENT_PERCENT = 0.10
# DEPRECIATION_SHORT_PERCENT = 0.08
# DEPRECIATION_LONG_PERCENT = 0.75
# TAX_BRACKET = 0.24
# IS_FIRST_RENTAL = True  # If 'False', halves emergency fund recommendation.
