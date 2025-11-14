import pytest
from atm_dataclass import ATMService, Money


def test_init_atm_service():
    initial_state = [
        Money(Values=5, Type="bill"),
        Money(Values=2, Type="coin"),
        Money(Values=50, Type="bill")
    ]
    atm = ATMService(initial_state=initial_state)
    assert atm.initial_state == [
            Money(Values=50, Type="bill"),
            Money(Values=5, Type="bill"),
            Money(Values=2, Type="coin")
        ]

def test_withdraw():
    atm = ATMService()
    assert atm.withdraw(604) == '1 bill of 500\n1 bill of 100\n2 coins of 2'
