import pandas as pd
from typing import Optional


class ATMServiceError(Exception):
    """Base ATM Service Error"""


class InsufficientATMCashError(ATMServiceError):
    pass


class ATMService:
    def __init__(
        self,
        values: list[int] = [500, 200, 100, 50, 20, 10, 5, 2, 1],
        values_type: list[str] = ["bill"] * 7 + ["coin", "coin"],
        values_qut: list[int] | None = [2, 3, 5, 12, 20, 50, 100, 250, 500]
    ) -> None:

        self._validate_list_of_values(values)
        self._validate_list_of_bills_or_coins(values_type)
        self._validate_list_of_quantities(values_qut)
        self._validate_lists_lenght(values, values_type, values_qut)
        self.values_qut = values_qut

        self.initial_state = pd.DataFrame({
            "Values": values,
            "Type": values_type
        }).sort_values(by=["Values"], ascending=False, ignore_index=True)

        self.initial_state_with_quantity = pd.DataFrame({
            "Values": values,
            "Type": values_type,
            "Quantity": values_qut
        }).sort_values(by=["Values"], ascending=False, ignore_index=True)

    def _validate_list_of_values(self, values_list: list[int]) -> bool:
        if not (isinstance(values_list, list) and all(isinstance(i, int) and i > 0 for i in values_list)):
            raise ValueError("The list of values must contain only positive integers.")
        return True

    def _validate_list_of_bills_or_coins(self, type_list: list[str]) -> bool:
        if not (isinstance(type_list, list) and all(i in {"bill", "coin"} for i in set(type_list))):
            raise ValueError("The list of types must contain only 'bill' or 'coin'.")
        return True

    def _validate_list_of_quantities(self, qut_list: Optional[list[int]] = None) -> bool:
        if qut_list and not (isinstance(qut_list, list) and all(isinstance(i, int) and i >= 0 for i in qut_list)):
            raise ValueError("The list of quantities must contain only integers equal to or greater than zero.")
        return True

    def _validate_lists_lenght(self, values_list: list[int], type_list: list[str], qut_list: Optional[list[int]] = None) -> None:
        if not qut_list and len(values_list) != len(type_list):
            raise ATMServiceError("The list of values must be the same length as the list of types.")
        if qut_list and not len(values_list) == len(type_list) == len(qut_list):
            raise ATMServiceError("The list of values must be the same length as the list of types and the list of quantities.")
        return True

    def withdraw(self, amount: int) -> str:
        self._validate_amount(amount)
        withdraw_statements = []
        for row in self.initial_state.itertuples(index=False):
            qut = amount // row.Values
            if qut > 0:
                amount -= qut * row.Values
                withdraw_statements.append(
                    f"{qut} {row.Type}{'s'[:qut^1]} of {row.Values}."
                )
            if amount <= 0:
                break
        return '\n'.join(withdraw_statements)

    def withdraw_with_quantity(self, amount: int) -> str:
        self._validate_amount(amount)
        self._validate_amount_available(amount)
        withdraw_statement = []
        for row in self.initial_state_with_quantity.itertuples():
            qut = min(amount // row.Values, row.Quantity)
            if qut > 0:
                amount -= qut * row.Values
                self.initial_state_with_quantity.loc[row.Index, "Quantity"] -= qut
                withdraw_statement.append(f"{qut} {row.Type}{'s'[:qut^1]} of {row.Values}.")
            if amount <= 0:
                break
        return '\n'.join(withdraw_statement)

    def _validate_amount_available(self, amount: int) -> None:
        if not self.values_qut or amount > sum(self.initial_state_with_quantity["Values"] * self.initial_state_with_quantity["Quantity"]):
            raise InsufficientATMCashError(
                "The ATM machine has not enough money, please go to the nearest atm machine"
            )

    def _validate_amount(self, amount: int) -> None:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Amount must be a positive integer.")
