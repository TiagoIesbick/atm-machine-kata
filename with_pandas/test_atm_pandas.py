import pytest
import pandas as pd
from atm_pandas import ATMService, ATMServiceError, InsufficientATMCashError


def test_init_atm_service():
    values = [5, 10, 3, 9]
    values_type = ["bill", "coin", "bill", "bill"]
    values_qut = [1, 0, 4, 6]
    atm = ATMService(values, values_type, values_qut)
    assert atm.initial_state.equals(pd.DataFrame({
        "Values": [10, 9, 5, 3],
        "Type": ["coin", "bill", "bill", "bill"]
    }))
    assert atm.initial_state_with_quantity.equals(pd.DataFrame({
        "Values": [10, 9, 5, 3],
        "Type": ["coin", "bill", "bill", "bill"],
        "Quantity": [0, 6, 1, 4]
    }))

def test_validate_list_of_values():
    atm = ATMService()
    with pytest.raises(ValueError):
        atm._validate_list_of_values([1, "a"])
    with pytest.raises(ValueError):
        atm._validate_list_of_values("hello")
    with pytest.raises(ValueError):
        atm._validate_list_of_values([1, -1])
    with pytest.raises(ValueError):
        atm._validate_list_of_values([1, 0])
    assert atm._validate_list_of_values([1,2])

def test_validate_list_of_quantities():
    atm = ATMService()
    with pytest.raises(ValueError):
        atm._validate_list_of_quantities([1, "a"])
    with pytest.raises(ValueError):
        atm._validate_list_of_quantities("hello")
    with pytest.raises(ValueError):
        atm._validate_list_of_quantities([1, -1])
    assert atm._validate_list_of_quantities([1,0])

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
        atm._validate_lists_lenght([1,2], ["a"])
    assert atm._validate_lists_lenght([1,2], ["a", "b"])
    with pytest.raises(ATMServiceError):
        atm._validate_lists_lenght([1,2], ["a", "b"], [1])
    assert atm._validate_lists_lenght([1,2], ["a", "b"], [1,2])

def test_withdraw():
    atm = ATMService()
    assert atm.withdraw(604) == '1 bill of 500.\n1 bill of 100.\n2 coins of 2.'
    assert atm.withdraw(434) == '2 bills of 200.\n1 bill of 20.\n1 bill of 10.\n2 coins of 2.'

def test_withdraw_with_quantity():
    atm = ATMService()
    assert atm.withdraw_with_quantity(1725) == '2 bills of 500.\n3 bills of 200.\n1 bill of 100.\n1 bill of 20.\n1 bill of 5.'
    assert atm.initial_state_with_quantity.equals(pd.DataFrame({
        "Values": [500, 200, 100, 50, 20, 10, 5, 2, 1],
        "Type": ["bill"] * 7 + ["coin", "coin"],
        "Quantity": [0, 0, 4, 12, 19, 50, 99, 250, 500]
    }))
    assert atm.withdraw_with_quantity(1825) == '4 bills of 100.\n12 bills of 50.\n19 bills of 20.\n44 bills of 10.\n1 bill of 5.'
    assert atm.initial_state_with_quantity.equals(pd.DataFrame({
        "Values": [500, 200, 100, 50, 20, 10, 5, 2, 1],
        "Type": ["bill"] * 7 + ["coin", "coin"],
        "Quantity": [0] * 5 + [6, 98, 250, 500]
    }))
    with pytest.raises(InsufficientATMCashError):
        atm.withdraw_with_quantity(1551)
    with pytest.raises(InsufficientATMCashError):
        ATMService(values_qut=None).withdraw_with_quantity(1)

def test_validate_amount():
    with pytest.raises(ValueError):
        ATMService()._validate_amount(0)
    with pytest.raises(ValueError):
        ATMService()._validate_amount(-1)
    with pytest.raises(ValueError):
        ATMService()._validate_amount("hello")
    with pytest.raises(ValueError):
        ATMService()._validate_amount(1.5)
    assert ATMService()._validate_amount(1) == None
