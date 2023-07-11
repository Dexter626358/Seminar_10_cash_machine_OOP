def check_sum(money: str):
    if money.isdigit() and int(money) > 0 and int(money) % 50 == 0:
        return True
    else:
        return False


def check_pin(number: str):
    if number.isdigit() and len(number) == 4:
        return True
    return False

