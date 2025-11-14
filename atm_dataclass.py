from dataclasses import dataclass
from typing import Literal


@dataclass
class Money:
    Values: int
    Type: Literal["bill", "coin"]


class ATMService:
    def __init__(
        self,
        initial_state: list[Money] = [
            Money(Values=500, Type="bill"),
            Money(Values=200, Type="bill"),
            Money(Values=100, Type="bill"),
            Money(Values=50, Type="bill"),
            Money(Values=20, Type="bill"),
            Money(Values=10, Type="bill"),
            Money(Values=5, Type="bill"),
            Money(Values=2, Type="coin"),
            Money(Values=1, Type="coin")
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

