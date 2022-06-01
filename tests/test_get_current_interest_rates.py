import pytest
from src.web.get_current_interest_rates import MortgageRates


@pytest.fixture(scope='session')
def interest_rates() -> dict:
    """Get the current interest rates once and use for all tests"""
    mortgage_rates = MortgageRates()
    mortgage_rates.set_interest_rates()
    interest_rates = mortgage_rates.interest_rates
    return interest_rates


def test_mortgage_rate_types(interest_rates) -> None:
    """Test if these rates were correctly found"""
    assert "30-year fixed-rate" in interest_rates
    assert "20-year fixed-rate" in interest_rates
    assert "15-year fixed-rate" in interest_rates
    assert "10-year fixed-rate" in interest_rates
    assert "7-year ARM" in interest_rates
    assert "5-year ARM" in interest_rates
    assert "3-year ARM" in interest_rates
    assert "30-year fixed-rate FHA" in interest_rates
    assert "30-year fixed-rate VA" in interest_rates


def test_mortgage_rates_valid(interest_rates) -> None:
    """Test if the rates are valid"""
    # Each rate should be a positive number
    for rate in interest_rates:
        assert float(interest_rates[rate]) > 0

    # Longer term loans should have higher interest. May not always be true so certain ones are skipped.
    assert interest_rates["30-year fixed-rate"] > interest_rates["20-year fixed-rate"]
    assert interest_rates["20-year fixed-rate"] > interest_rates["15-year fixed-rate"]
    assert interest_rates["7-year ARM"] > interest_rates["5-year ARM"]
    assert interest_rates["5-year ARM"] > interest_rates["3-year ARM"]
    