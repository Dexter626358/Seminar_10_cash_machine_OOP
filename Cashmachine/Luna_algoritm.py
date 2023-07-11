import random


def create_card_number():
    """Этот метод генерирует случайный 16-значный номер кредитной карты и вычисляет последнюю цифру
     (контрольную сумму) с помощью алгоритма Луна.
    В результате получается валидный номер кредитной карты."""
    # Генерируем первые 15 цифр случайным образом
    card_number = str(random.randint(1, 9))
    for _ in range(14):
        card_number += str(random.randint(0, 9))

    # Вычисляем последнюю цифру (контрольную сумму) с помощью алгоритма Луна
    digits = [int(x) for x in card_number]
    for i in range(0, 15, 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    checksum = sum(digits) % 10
    if checksum != 0:
        checksum = 10 - checksum

    card_number += str(checksum)

    return card_number
