class CreditCardValidator:
    @staticmethod
    def is_valid(card_number):
        # Удаляем пробелы и дефисы из номера карты
        card_number = card_number.replace(" ", "").replace("-", "")

        # Проверяем, является ли номер карты числом
        if not card_number.isdigit():
            return False

        # Переворачиваем номер карты и преобразуем в список цифр
        digits = [int(digit) for digit in card_number[::-1]]

        # Удваиваем каждую вторую цифру
        doubled_digits = []
        for i in range(len(digits)):
            if i % 2 == 1:
                doubled_digit = digits[i] * 2
                doubled_digits.append(doubled_digit if doubled_digit < 10 else doubled_digit - 9)
            else:
                doubled_digits.append(digits[i])

        # Суммируем все цифры
        total = sum(doubled_digits)

        # Проверяем, что сумма кратна 10
        return total % 10 == 0