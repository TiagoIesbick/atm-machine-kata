import pytest
import pandas as pd
from atm_pandas import ATMService, ATMServiceError


def test_init_atm_service():
    values = [5, 10, 3, 9]
    values_type = ["bill", "coin", "bill", "bill"]
    atm = ATMService(values, values_type)
    assert atm.initial_state.equals(pd.DataFrame({
        "Values": [10, 9, 5, 3],
        "Type": ["coin", "bill", "bill", "bill"]
    }))

def test_validate_list_of_ints():
    atm = ATMService()
    with pytest.raises(ValueError):
        atm._validate_list_of_ints([1, "a"])
    with pytest.raises(ValueError):
        atm._validate_list_of_ints("hello")
    with pytest.raises(ValueError):
        atm._validate_list_of_ints([1, -1])
    with pytest.raises(ValueError):
        atm._validate_list_of_ints([1, 0])
    assert atm._validate_list_of_ints([1,2])

def test_validate_list_of_bills_or_coins():
    atm = ATMService()
    with pytest.raises(ValueError):
        atm._validate_list_of_bills_or_coins(["bill", "coin", "hello"])
    with pytest.raises(ValueError):
        atm._validate_list_of_bills_or_coins("hello")
    assert atm._validate_list_of_bills_or_coins(["bill", "coin"])

def test_validate_lists_lenght():
    atm = ATMService()
    with pytest.raises(ATMServiceError):
        atm._validate_lists_lenght([1,2], [1])
    assert atm._validate_lists_lenght([1,2], ["a", "b"])

def test_withdraw():
    atm = ATMService()
    assert atm.withdraw(604) == '1 bill of 500.\n1 bill of 100.\n2 coins of 2.'
    assert atm.withdraw(434) == '2 bills of 200.\n1 bill of 20.\n1 bill of 10.\n2 coins of 2.'