import random
from Card import Card
from Cashmachine.Counter import Counter
from cashmachine import Cashmachine
from Luna_algoritm import create_card_number
from Checker import check_pin, check_sum
from CreditCardValidator import CreditCardValidator


def main_menu():
    return f"1. Обратиться в банк.\n2. Выбрать банкомат.\n3. Выйти.\n"


def bank_menu():
    return f"1. Выпустить карту.\n2. Вернуться в главное меню.\n"


def cash_machine_menu():
    return f"1. Пополнить счет.\n2. Снять деньги со счета.\n3. Вывести баланс.\n4. Выйти.\n"


def interest_money(sum_withdraw):
    interest_rate = 1.5
    charge_money = sum_withdraw * interest_rate / 100
    if charge_money < 30:
        charge_money = 30
    if charge_money > 600:
        charge_money = 600
    return charge_money


class UserInterface:
    card_status = False
    count_operations = 0

    def create_cash_machines(self):
        cash_machins_storage = []
        for i in range(1000, 1011):
            cash_machins_storage.append(Cashmachine(i, random.randint(5_000_000, 10_000_000)))
        return cash_machins_storage

    def run(self):
        cash_m = self.create_cash_machines()
        card_holder = []
        counter_operations = Counter()
        incorrect_input = "Введено некорректное значение. Попробуйте снова."
        while True:
            print(main_menu())
            main_choose = input()
            if main_choose == "1":  # выпустить карту
                while True:
                    card_holder.append(Card("1234123412341234", 0, 1234))
                    print(bank_menu())
                    bank_choose = input()
                    if bank_choose == "1":  # выпуск карты
                        pin = random.randint(1000, 9999)
                        card_holder.append(Card(create_card_number(), 0, pin))
                        print(f"Выпущeна карта с номером {card_holder[-1].number} и пин-кодом {card_holder[-1].pin}")
                    elif bank_choose == "2":  # вернуться в главное меню
                        break
                    else:
                        print(incorrect_input)
            elif main_choose == "2":  # выбрать банкомат
                ind_cash_machine = -1
                while True:
                    print("1 - вывести список банкоматов, 2 - выйти.")
                    bancomat = input()
                    if bancomat == "1":
                        print("Выберите банкомат")
                        for key in cash_m:
                            print(f"Банкомат № {key.id}")
                        cash_mach_choose = input()
                        for ind in range(0, len(cash_m)):
                            if cash_mach_choose == str(cash_m[ind].id):
                                ind_cash_machine = ind
                                break
                        if ind_cash_machine == -1:
                            print("Банкомата с таким номером не существует")
                            continue
                    elif bancomat == "2":
                        break
                    else:
                        print(incorrect_input)
                    print("Вставьте карту в банкомат. Для продолжения нажмите enter...")
                    put_card = input()
                    while True:
                        index_card = -1
                        print("Введите номер карты: ")
                        get_card_number = input()
                        if CreditCardValidator.is_valid(get_card_number):
                            for i in range(0, len(card_holder)):
                                if card_holder[i].number == get_card_number:
                                    index_card = i
                                    break
                            if index_card == -1:
                                print("Карта с таким номером не найдена")
                                continue
                            break
                        else:
                            print("Введен некорректный номер карты. Попробуйте снова.")
                    while True:
                        print("Введите пин-код: ")
                        get_pin_number = input()
                        if check_pin(get_pin_number) and card_holder[index_card].pin == int(get_pin_number):
                            card_status = True
                            print("Пин-код принят")
                            break
                        else:
                            print("Введен неверный пин-код. Пин-код должен содержать 4 цифры.")
                    while card_status:
                        print(cash_machine_menu())
                        cash_machine_choose = input()
                        if cash_machine_choose == "1":  # пополнить счет
                            while True:
                                print("Введите сумму, кратную 50$, которую Вы хотите положить на счет.")
                                str_money = input()
                                if check_sum(str_money):
                                    card_holder[index_card].add_money(int(str_money))
                                    print("Счет пополнен.")
                                    cash_m[ind_cash_machine].add_money(int(str_money))
                                    counter_operations.increment(card_holder[index_card])
                                    if card_holder[index_card].show_balance() > 5_000_000:
                                        print(card_holder[index_card].taxis_on_richness())
                                    break
                                else:
                                    print("Некорректная сумма. Попробуйте снова.")
                        elif cash_machine_choose == "2":  # снять деньги
                            while True:
                                print("Введите сумму, кратную 50$, которую Вы хотите снять со счета.")
                                str_money = input()
                                if check_sum(str_money):
                                    charge_money_ = interest_money(int(str_money))
                                    if cash_m[ind_cash_machine].money_on_count < int(str_money) + charge_money_:
                                        print("В банкомате недостаточно средств")
                                        break
                                    else:
                                        if card_holder[index_card].show_balance() >= int(str_money) + charge_money_:
                                            card_holder[index_card].withdraw_money((int(str_money)) + charge_money_)
                                            print(
                                                f"Операция выполнена успешно с комиссией {round(charge_money_, 2)}$\n")
                                            print("Возьмите деньги.")
                                            cash_m[ind_cash_machine].withdraw_money((int(str_money)) + charge_money_)
                                            counter_operations.increment(card_holder[index_card])
                                        else:
                                            print("У Вас недостаточно средств на счете для осуществления операции.\n")
                                        break
                                else:
                                    print("Некорректная сумма. Попробуйте снова.")
                        elif cash_machine_choose == "3":  # вывести баланс
                            print(f"Баланс карты равен: {card_holder[index_card].show_balance()}$")
                            counter_operations.increment(card_holder[index_card])

                        elif cash_machine_choose == "4":  # выход
                            print("Заберите карту из банкомата.")
                            card_status = False
                        else:
                            print(incorrect_input)
            elif main_choose == "3":  # выход из программы
                break
            else:
                print(incorrect_input)


ui = UserInterface()
ui.run()
