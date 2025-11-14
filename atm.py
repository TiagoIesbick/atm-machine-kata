import pandas as pd


class ATMServiceError(Exception):
    """Base ATM Service Error"""


class ATMService:
    def __init__(
        self,
        values: list[int] = [500, 200, 100, 50, 20, 10, 5, 2, 1],
        values_type: list[str] = ["bill", "bill", "bill", "bill", "bill", "bill", "bill", "coin", "coin"]
    ) -> None:

        self._validate_list_of_ints(values)
        self._validate_list_of_bills_or_coins(values_type)
        self._validate_lists_lenght(values, values_type)

        self.initial_state = pd.DataFrame({
            "Values": values,
            "Type": values_type
        }).sort_values(by=["Values"], ascending=False, ignore_index=True)

    def _validate_list_of_ints(self, int_list: list[int]) -> bool:
        if not (isinstance(int_list, list) and all(isinstance(i, int) for i in int_list)):
            raise ValueError("The list of values must contain only integers.")
        return True

    def _validate_list_of_bills_or_coins(self, money_type_list: list[str]) -> bool:
        if not (isinstance(money_type_list, list) and all(i in {"bill", "coin"} for i in set(money_type_list))):
            raise ValueError("The list of types must contain only 'bill' or 'coin'.")
        return True

    def _validate_lists_lenght(self, list1: list, list2: list) -> bool:
        if not len(list1) == len(list2):
            raise ATMServiceError("The list of values must be the same length as the list of types.")
        return True

    def withdraw(self, amount: int) -> str:
        withdraw_statements = []
        for row in self.initial_state.itertuples(index=False):
            qut = amount // row.Values
            if qut > 0:
                amount -= qut * row.Values
                withdraw_statements.append(
                    f"{qut} {row.Type}{'s'[:qut^1]} of {row.Values}"
                )
        return '\n'.join(withdraw_statements)
