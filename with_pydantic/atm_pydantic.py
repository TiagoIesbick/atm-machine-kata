from pydantic import BaseModel, Field, PositiveInt
from typing import Literal


class MoneyPydantic(BaseModel):
    Values: PositiveInt = Field(description="Positive integer monetary value.")
    Type: Literal["bill", "coin"] = Field(description="Money type.")


class MoneyPydanticWithQuantity(MoneyPydantic):
    Quantity: int = Field(ge=0, description="Quantity of the type of money available.")


class InsufficientATMCashError(Exception):
    pass


class ATMServicePydantic:
    def __init__(
        self,
        initial_state: list[MoneyPydantic] = [
            MoneyPydantic(Values=500, Type="bill"),
            MoneyPydantic(Values=200, Type="bill"),
            MoneyPydantic(Values=100, Type="bill"),
            MoneyPydantic(Values=50, Type="bill"),
            MoneyPydantic(Values=20, Type="bill"),
            MoneyPydantic(Values=10, Type="bill"),
            MoneyPydantic(Values=5, Type="bill"),
            MoneyPydantic(Values=2, Type="coin"),
            MoneyPydantic(Values=1, Type="coin")
        ],
        initial_state_with_quantity: list[MoneyPydanticWithQuantity] = [
            MoneyPydanticWithQuantity(Values=500, Type="bill", Quantity=2),
            MoneyPydanticWithQuantity(Values=200, Type="bill", Quantity=3),
            MoneyPydanticWithQuantity(Values=100, Type="bill", Quantity=5),
            MoneyPydanticWithQuantity(Values=50, Type="bill", Quantity=12),
            MoneyPydanticWithQuantity(Values=20, Type="bill", Quantity=20),
            MoneyPydanticWithQuantity(Values=10, Type="bill", Quantity=50),
            MoneyPydanticWithQuantity(Values=5, Type="bill", Quantity=100),
            MoneyPydanticWithQuantity(Values=2, Type="coin", Quantity=250),
            MoneyPydanticWithQuantity(Values=1, Type="coin", Quantity=500)
        ]
    ) -> None:
        self.initial_state = sorted(initial_state, key=lambda x: x.Values, reverse=True)
        self.initial_state_with_quantity = sorted(initial_state_with_quantity, key=lambda x: x.Values, reverse=True)

    def withdraw(self, amount: int) -> str:
        withdraw_statement = []
        for money in self.initial_state:
            qut = amount // money.Values
            if qut > 0:
                amount -= qut * money.Values
                withdraw_statement.append(f"{qut} {money.Type}{'s'[:qut^1]} of {money.Values}.")
        return '\n'.join(withdraw_statement)

    def withdraw_with_quantity(self, amount: int) -> str:
        self._validate_amount_available(amount)
        withdraw_statement = []
        for money in self.initial_state_with_quantity:
            qut = min(amount // money.Values, money.Quantity)
            if qut > 0:
                amount -= qut * money.Values
                money.Quantity -= qut
                withdraw_statement.append(f"{qut} {money.Type}{'s'[:qut^1]} of {money.Values}.")
        return '\n'.join(withdraw_statement)

    def _validate_amount_available(self, amount: int) -> None:
        if amount > sum(m.Values * m.Quantity for m in self.initial_state_with_quantity):
            raise InsufficientATMCashError(
                "The ATM machine has not enough money, please go to the nearest atm machine"
            )
