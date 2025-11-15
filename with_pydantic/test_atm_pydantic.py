import pytest
from atm_pydantic import ATMServicePydantic, MoneyPydantic, MoneyPydanticWithQuantity, InsufficientATMCashError
from pydantic import ValidationError


def test_init_atm_service():
    initial_state = [
        MoneyPydantic(Values=5, Type="bill"),
        MoneyPydantic(Values=2, Type="coin"),
        MoneyPydantic(Values=50, Type="bill")
    ]
    initial_state_with_quantity = [
        MoneyPydanticWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyPydanticWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=0)
    ]
    atm = ATMServicePydantic(
        initial_state=initial_state,
        initial_state_with_quantity=initial_state_with_quantity
    )
    assert atm.initial_state == [
            MoneyPydantic(Values=50, Type="bill"),
            MoneyPydantic(Values=5, Type="bill"),
            MoneyPydantic(Values=2, Type="coin")
        ]
    assert atm.initial_state_with_quantity == [
        MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyPydanticWithQuantity(Values=2, Type="coin", Quantity=250)
    ]
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=0, Type="bill")])
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=-1, Type="bill")])
    with pytest.raises(ValidationError):
        ATMServicePydantic(initial_state=[MoneyPydantic(Values=5, Type="hello")])
    with pytest.raises(ValueError):
        ATMServicePydantic(
            initial_state_with_quantity=MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=-1)
        )

def test_withdraw():
    atm = ATMServicePydantic()
    assert atm.withdraw(604) == '1 bill of 500.\n1 bill of 100.\n2 coins of 2.'
    assert atm.withdraw(434) == '2 bills of 200.\n1 bill of 20.\n1 bill of 10.\n2 coins of 2.'

def test_withdraw_with_quantity():
    atm = ATMServicePydantic()
    assert atm.withdraw_with_quantity(1725) == '2 bills of 500.\n3 bills of 200.\n1 bill of 100.\n1 bill of 20.\n1 bill of 5.'
    assert atm.initial_state_with_quantity == [
        MoneyPydanticWithQuantity(Values=500, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=200, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=4),
        MoneyPydanticWithQuantity(Values=50, Type="bill", Quantity=12),
        MoneyPydanticWithQuantity(Values=20, Type="bill", Quantity=19),
        MoneyPydanticWithQuantity(Values=10, Type="bill", Quantity=50),
        MoneyPydanticWithQuantity(Values=5, Type="bill", Quantity=99),
        MoneyPydanticWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyPydanticWithQuantity(Values=1, Type="coin", Quantity=500)
    ]
    assert atm.withdraw_with_quantity(1825) == '4 bills of 100.\n12 bills of 50.\n19 bills of 20.\n44 bills of 10.\n1 bill of 5.'
    assert atm.initial_state_with_quantity == [
        MoneyPydanticWithQuantity(Values=500, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=200, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=50, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=20, Type="bill", Quantity=0),
        MoneyPydanticWithQuantity(Values=10, Type="bill", Quantity=6),
        MoneyPydanticWithQuantity(Values=5, Type="bill", Quantity=98),
        MoneyPydanticWithQuantity(Values=2, Type="coin", Quantity=250),
        MoneyPydanticWithQuantity(Values=1, Type="coin", Quantity=500)
    ]
    with pytest.raises(InsufficientATMCashError):
        atm.withdraw_with_quantity(1551)
