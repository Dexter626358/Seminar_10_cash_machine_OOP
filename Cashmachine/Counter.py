class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, card):
        self.count += 1
        if self.count == 3:
            self.execute_action(card)
            self.count = 0

    def execute_action(self, card):
        card.withdraw_money(round(card.show_balance() * 0.03))
        print(f"Комиссия за выполнение 3х и более операций в размере {round(card.show_balance() * 0.03, 2)}$\n")

