import datetime
import random
from Card import Card
from Cashmachine.Counter import Counter
from cashmachine import Cashmachine
from Luna_algoritm import create_card_number
from Checker import check_pin, check_sum
from CreditCardValidator import CreditCardValidator
import logging


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


logging.basicConfig(filename='errors.log',
                    filemode='a',
                    encoding='utf-8',
                    style='{',
                    level=logging.INFO)
logger = logging.getLogger()


class UserInterface:
    card_status = False
    count_operations = 0

    def create_cash_machines(self):
        cash_machins_storage = []
        for i in range(1000, 1011):
            cash_machins_storage.append(Cashmachine(i, random.randint(5_000_000, 10_000_000)))
        return cash_machins_storage

    def run(self):
        logger.info(f"Старт работы программы в {datetime.datetime.now()}")
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
                        logger.info(f"Успешно выпущена карта в {datetime.datetime.now()}")
                    elif bank_choose == "2":  # вернуться в главное меню
                        logger.info(f"Возврат в главное меню в {datetime.datetime.now()}")
                        break
                    else:
                        print(incorrect_input)
                        logger.info(f"Некорректный ввод данных в {datetime.datetime.now()}")
            elif main_choose == "2":  # выбрать банкомат
                ind_cash_machine = -1
                while True:
                    print("1 - вывести список банкоматов, 2 - выйти.")
                    bancomat = input()
                    if bancomat == "1":
                        print("Выберите банкомат")
                        for key in cash_m:
                            print(f"Банкомат № {key.id}")
                        logger.info(f"Выведен список банкоматов в {datetime.datetime.now()}")
                        cash_mach_choose = input()
                        for ind in range(0, len(cash_m)):
                            if cash_mach_choose == str(cash_m[ind].id):
                                ind_cash_machine = ind
                                logger.info(f"Успешно выбран банкомат в {datetime.datetime.now()}")
                                break
                        if ind_cash_machine == -1:
                            print("Банкомата с таким номером не существует")
                            logger.info(f"Некорректный ввод данных(выбор банкомата) в {datetime.datetime.now()}")
                            continue
                    elif bancomat == "2":
                        break
                    else:
                        print(incorrect_input)
                    print("Вставьте карту в банкомат. Для продолжения нажмите enter...")
                    logger.info(f"Карта вставлена в банкомат в {datetime.datetime.now()}")
                    put_card = input()
                    while True:
                        index_card = -1
                        print("Введите номер карты: ")
                        get_card_number = input()
                        if CreditCardValidator.is_valid(get_card_number):
                            for i in range(0, len(card_holder)):
                                if card_holder[i].number == get_card_number:
                                    index_card = i
                                    logger.info(f"Успешно введен номер карты в {datetime.datetime.now()}")
                                    break
                            if index_card == -1:
                                print("Карта с таким номером не найдена")
                                logger.info(f"Номер карты не прошел проверку в {datetime.datetime.now()}")
                                continue
                            break
                        else:
                            print("Введен некорректный номер карты. Попробуйте снова.")
                            logger.info(f"Введен некорректный номер карты в {datetime.datetime.now()}")

                    while True:
                        print("Введите пин-код: ")
                        get_pin_number = input()
                        if check_pin(get_pin_number) and card_holder[index_card].pin == int(get_pin_number):
                            card_status = True
                            print("Пин-код принят")
                            logger.info(f"Пин-код введен успешно в {datetime.datetime.now()}")
                            break
                        else:
                            print("Введен неверный пин-код. Пин-код должен содержать 4 цифры.")
                            logger.info(f"Введен неверный пин-код в {datetime.datetime.now()}")
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
                                    logger.info(f"Счет успешно пополнен в {datetime.datetime.now()}")
                                    cash_m[ind_cash_machine].add_money(int(str_money))
                                    counter_operations.increment(card_holder[index_card])
                                    if card_holder[index_card].show_balance() > 5_000_000:
                                        print(card_holder[index_card].taxis_on_richness())
                                    break
                                else:
                                    print("Некорректная сумма. Попробуйте снова.")
                                    logger.info(f"Введена некорректная сумма при пополнении счета в {datetime.datetime.now()}")
                        elif cash_machine_choose == "2":  # снять деньги
                            while True:
                                print("Введите сумму, кратную 50$, которую Вы хотите снять со счета.")
                                str_money = input()
                                if check_sum(str_money):
                                    charge_money_ = interest_money(int(str_money))
                                    if cash_m[ind_cash_machine].money_on_count < int(str_money) + charge_money_:
                                        print("В банкомате недостаточно средств")
                                        logger.info(f"В банкомате недостаточно средств в {datetime.datetime.now()}")
                                        break
                                    else:
                                        if card_holder[index_card].show_balance() >= int(str_money) + charge_money_:
                                            card_holder[index_card].withdraw_money((int(str_money)) + charge_money_)
                                            print(
                                                f"Операция выполнена успешно с комиссией {round(charge_money_, 2)}$\n")
                                            logger.info(f"Списание комиссии в {datetime.datetime.now()}")
                                            print("Возьмите деньги.")
                                            cash_m[ind_cash_machine].withdraw_money((int(str_money)) + charge_money_)
                                            counter_operations.increment(card_holder[index_card])
                                        else:
                                            print("У Вас недостаточно средств на счете для осуществления операции.\n")
                                            logger.info(f"Не удалось снять деньги. На счету недостаточно средств"
                                                        f"  в {datetime.datetime.now()}")
                                        break
                                else:
                                    print("Некорректная сумма. Попробуйте снова.")
                                    logger.info(f"Ввод некорректной суммы для снятия средств в {datetime.datetime.now()}")
                        elif cash_machine_choose == "3":  # вывести баланс
                            print(f"Баланс карты равен: {card_holder[index_card].show_balance()}$")
                            logger.info(f"Проверка баланса карты в {datetime.datetime.now()}")
                            counter_operations.increment(card_holder[index_card])

                        elif cash_machine_choose == "4":  # выход
                            print("Заберите карту из банкомата.")
                            card_status = False
                        else:
                            print(incorrect_input)
            elif main_choose == "3":  # выход из программы
                logger.info(f"Выход из программы в {datetime.datetime.now()}")
                break
            else:
                print(incorrect_input)
                logger.info(f"Некорректный ввод данных в {datetime.datetime.now()}")


ui = UserInterface()
ui.run()
