import pytest
from atm_dataclass import ATMServiceDataClass, MoneyDataClass


def test_init_atm_service():
    initial_state = [
        MoneyDataClass(Values=5, Type="bill"),
        MoneyDataClass(Values=2, Type="coin"),
        MoneyDataClass(Values=50, Type="bill")
    ]
    atm = ATMServiceDataClass(initial_state=initial_state)
    assert atm.initial_state == [
            MoneyDataClass(Values=50, Type="bill"),
            MoneyDataClass(Values=5, Type="bill"),
            MoneyDataClass(Values=2, Type="coin")
        ]
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=0, Type="bill")])
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=-1, Type="bill")])
    with pytest.raises(ValueError):
        ATMServiceDataClass(initial_state=[MoneyDataClass(Values=5, Type="hello")])

def test_withdraw():
    atm = ATMServiceDataClass()
    assert atm.withdraw(604) == '1 bill of 500\n1 bill of 100\n2 coins of 2'
