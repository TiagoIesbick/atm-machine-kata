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


@dataclass
class MoneyDataClassWithQuantity(MoneyDataClass):
    Quantity: int

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.Quantity, int) or self.Quantity < 0:
            raise ValueError("Quantity must be equal to or greater than zero.")


class InsufficientATMCashError(Exception):
    pass


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
        ],
        initial_state_with_quantity: list[MoneyDataClassWithQuantity] = [
            MoneyDataClassWithQuantity(Values=500, Type="bill", Quantity=2),
            MoneyDataClassWithQuantity(Values=200, Type="bill", Quantity=3),
            MoneyDataClassWithQuantity(Values=100, Type="bill", Quantity=5),
            MoneyDataClassWithQuantity(Values=50, Type="bill", Quantity=12),
            MoneyDataClassWithQuantity(Values=20, Type="bill", Quantity=20),
            MoneyDataClassWithQuantity(Values=10, Type="bill", Quantity=50),
            MoneyDataClassWithQuantity(Values=5, Type="bill", Quantity=100),
            MoneyDataClassWithQuantity(Values=2, Type="coin", Quantity=250),
            MoneyDataClassWithQuantity(Values=1, Type="coin", Quantity=500)
        ]
    ) -> None:
        self.initial_state = sorted(initial_state, key=lambda x: x.Values, reverse=True)
        self.initial_state_with_quantity = sorted(initial_state_with_quantity, key=lambda x: x.Values, reverse=True)

    def withdraw(self, amount: int) -> str:
        self._validate_amount(amount)
        withdraw_statement = []
        for money in self.initial_state:
            qut = amount // money.Values
            if qut > 0:
                amount -= qut * money.Values
                withdraw_statement.append(f"{qut} {money.Type}{'s'[:qut^1]} of {money.Values}.")
            if amount <= 0:
                break
        return '\n'.join(withdraw_statement)

    def withdraw_with_quantity(self, amount: int) -> str:
        self._validate_amount(amount)
        self._validate_amount_available(amount)
        withdraw_statement = []
        for money in self.initial_state_with_quantity:
            qut = min(amount // money.Values, money.Quantity)
            if qut > 0:
                amount -= qut * money.Values
                money.Quantity -= qut
                withdraw_statement.append(f"{qut} {money.Type}{'s'[:qut^1]} of {money.Values}.")
            if amount <= 0:
                break
        return '\n'.join(withdraw_statement)

    def _validate_amount_available(self, amount: int) -> None:
        if amount > sum(m.Values * m.Quantity for m in self.initial_state_with_quantity):
            raise InsufficientATMCashError(
                "The ATM machine has not enough money, please go to the nearest atm machine"
            )

    def _validate_amount(self, amount: int) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer.")
