"""DEFAULT VALUES USED FOR ANALYSIS. CHANGE THESE VALUES ACCORDING TO YOUR HEURISTICS. TOUCH NOTHING ELSE."""


DOWN_PAYMENT_PERCENT = 0.20
YEARS = 30  # 'FHA' and 'VA' requires YEARS = 30. 'Conventional' has options for YEARS = 30, 20, 15, 10.
LOAN_TYPE = 'Conventional'  # Options are 'Conventional', 'FHA', 'VA'. !!! NOTE: 'FHA' and 'VA' requires YEARS = 30.
PROPERTY_TAXES = 4000
FIX_UP_COST = 10000
CLOSING_PERCENT = 0.03
NUM_UNITS = 3
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
