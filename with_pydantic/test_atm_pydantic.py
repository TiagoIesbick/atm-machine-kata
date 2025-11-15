import pytest
from atm_pydantic import ATMServicePydantic, MoneyPydantic
from pydantic import ValidationError


def test_init_atm_service():
    initial_state = [
        MoneyPydantic(Values=5, Type="bill"),
        MoneyPydantic(Values=2, Type="coin"),
        MoneyPydantic(Values=50, Type="bill")
    ]
    atm = ATMServicePydantic(initial_state=initial_state)
    assert atm.initial_state == [
            MoneyPydantic(Values=50, Type="bill"),
            MoneyPydantic(Values=5, Type="bill"),
            MoneyPydantic(Values=2, Type="coin")
        ]
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=0, Type="bill")])
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=-1, Type="bill")])
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=5, Type="hello")])

def test_withdraw():
    atm = ATMServicePydantic()
    assert atm.withdraw(604) == '1 bill of 500\n1 bill of 100\n2 coins of 2'
