from Cashmachine.Checker import check_sum


class Card:
    def __init__(self, number, amount_money, pin):
        self.number = number
        self.amount_money = amount_money
        self.pin = pin

    def add_money(self, amount_money):
        self.amount_money += amount_money

    def withdraw_money(self, amount_money):
        self.amount_money -= amount_money

    def show_balance(self):
        return self.amount_money

    def taxis_on_richness(self):
        self.amount_money -= self.amount_money * 0.05
        return f"Списание налога на богатство в размере {round(self.amount_money * 0.05, 2)}$\n"



