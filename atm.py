import pandas as pd


class ATMService:
    def __init__(self) -> None:
        self.initial_state = pd.DataFrame({
            "Values": [500, 200, 100, 50, 20, 10, 5, 2, 1],
            "Type": ["bill", "bill", "bill", "bill", "bill", "bill", "bill", "coin", "coin" ]
        })

    def withdraw(self, amount: int):
        for i in self.initial_state["Values"]:
            qut = amount // i
            amount -= qut*i
            if qut > 0:
                print(f"{qut} {self.initial_state.loc[self.initial_state["Values"] == i, "Type"].values[0]}{'s'[:qut^1]} of {i}")


atm = ATMService()
atm.withdraw(434)

amount = 434

# for i in atm.initial_state["Values"]:
#     if i > amount:
#         pass
#     elif i < amount:
#         qut = amount // i
#         amount -= qut*i
#         print(qut, amount)
#         print(f"{qut} {atm.initial_state.loc[atm.initial_state["Values"] == i, "Type"].values[0]}")