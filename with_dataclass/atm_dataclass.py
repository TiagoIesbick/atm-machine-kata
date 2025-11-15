from dataclasses import dataclass
from typing import Literal


@dataclass
class MoneyDataClass:
    Values: int
    Type: Literal["bill", "coin"]

    def __post_init__(self):
        if not isinstance(self.Values, int) or self.Values <= 0:
            raise ValueError("Values must be a positive integer.")

        if self.Type not in {"bill", "coin"}:
            raise ValueError("Type must be either 'bill' or 'coin'.")


class ATMServiceDataClass:
    def __init__(
        self,
        initial_state: list[MoneyDataClass] = [
            MoneyDataClass(Values=500, Type="bill"),
            MoneyDataClass(Values=200, Type="bill"),
            MoneyDataClass(Values=100, Type="bill"),
            MoneyDataClass(Values=50, Type="bill"),
            MoneyDataClass(Values=20, Type="bill"),
            MoneyDataClass(Values=10, Type="bill"),
            MoneyDataClass(Values=5, Type="bill"),
            MoneyDataClass(Values=2, Type="coin"),
            MoneyDataClass(Values=1, Type="coin")
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
