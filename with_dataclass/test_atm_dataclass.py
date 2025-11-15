import pytest
from atm_dataclass import ATMServiceDataClass, MoneyDataClass, MoneyDataClassWithQuantity, InsufficientATMCashError


def test_init_atm_service():
    initial_state = [
        MoneyDataClass(Values=5, Type="bill"),
        MoneyDataClass(Values=2, Type="coin"),
        MoneyDataClass(Values=50, Type="bill")
    ]
    initial_state_with_quantity = [
        MoneyDataClassWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyDataClassWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=0)
    ]
    atm = ATMServiceDataClass(
        initial_state=initial_state,
        initial_state_with_quantity=initial_state_with_quantity
    )
    assert atm.initial_state == [
            MoneyDataClass(Values=50, Type="bill"),
            MoneyDataClass(Values=5, Type="bill"),
            MoneyDataClass(Values=2, Type="coin")
        ]
    assert atm.initial_state_with_quantity == [
        MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyDataClassWithQuantity(Values=2, Type="coin", Quantity=250)
    ]
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=0, Type="bill")])
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=-1, Type="bill")])
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=5, Type="hello")])
    with pytest.raises(ValueError):
        ATMServiceDataClass(
            initial_state_with_quantity=MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=-1)
        )

def test_withdraw():
    atm = ATMServiceDataClass()
    assert atm.withdraw(604) == '1 bill of 500.\n1 bill of 100.\n2 coins of 2.'
    assert atm.withdraw(434) == '2 bills of 200.\n1 bill of 20.\n1 bill of 10.\n2 coins of 2.'

def test_withdraw_with_quantity():
    atm = ATMServiceDataClass()
    assert atm.withdraw_with_quantity(1725) == '2 bills of 500.\n3 bills of 200.\n1 bill of 100.\n1 bill of 20.\n1 bill of 5.'
    assert atm.initial_state_with_quantity == [
        MoneyDataClassWithQuantity(Values=500, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=200, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=4),
        MoneyDataClassWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyDataClassWithQuantity(Values=20, Type="bill", Quantity=19),
        MoneyDataClassWithQuantity(Values=10, Type="bill", Quantity=50),
        MoneyDataClassWithQuantity(Values=5, Type="bill", Quantity=99),
        MoneyDataClassWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyDataClassWithQuantity(Values=1, Type="coin", Quantity=500)
    ]
    assert atm.withdraw_with_quantity(1825) == '4 bills of 100.\n12 bills of 50.\n19 bills of 20.\n44 bills of 10.\n1 bill of 5.'
    assert atm.initial_state_with_quantity == [
        MoneyDataClassWithQuantity(Values=500, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=200, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=50, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=20, Type="bill", Quantity=0),
        MoneyDataClassWithQuantity(Values=10, Type="bill", Quantity=6),
        MoneyDataClassWithQuantity(Values=5, Type="bill", Quantity=98),
        MoneyDataClassWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyDataClassWithQuantity(Values=1, Type="coin", Quantity=500)
    ]
    with pytest.raises(InsufficientATMCashError):
        atm.withdraw_with_quantity(1551)
