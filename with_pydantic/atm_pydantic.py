from pydantic import BaseModel, Field, PositiveInt
from typing import Literal


class MoneyPydantic(BaseModel):
    Values: PositiveInt = Field(description="Positive integer monetary value.")
    Type: Literal["bill", "coin"] = Field(description="Money type.")


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
        ]
    ) -> None:
        self.initial_state = sorted(initial_state, key=lambda x: x.Values, reverse=True)

    def withdraw(self, amount: int) -> str:
        withdraw_statement = []
        for money in self.initial_state:
            qut = amount // money.Values
            if qut > 0:
                amount -= qut * money.Values
                withdraw_statement.append(f"{qut} {money.Type}{'s'[:qut^1]} of {money.Values}")
        return '\n'.join(withdraw_statement)
