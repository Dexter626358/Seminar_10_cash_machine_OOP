class Cashmachine:

    def __init__(self, id, money_on_count):
        self.id = id
        self.money_on_count = money_on_count

    def withdraw_money(self, money):
        self.money_on_count -= money

    def show_balance(self):
        return self.money_on_count

    def add_money(self, money):
        self.money_on_count -= money
