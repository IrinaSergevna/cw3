from datetime import datetime

class Payment:
    """Карта, номер"""

    def __init__(self, name, number):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name
        self.number = number


    @classmethod
    def init_from_str(cls, payment):
        """Принимает строку в формате "Счет 75106830613657916952". Возвращает список ["Счет", "75106830613657916952"]
        """
        *name, number = payment.split(' ')
        return cls(' '.join(name), number)


    def __repr__(self):  # pragma: nocover
        return f'Payment(name={self.name}, number={self.number})'


    def safe(self):
        """Возвращает строки <откуда> и <куда> в заданном формате"""
        if self.name.lower() == 'счет':
            safe_number = self.get_safe_account()
        else:
            safe_number = self.get_safe_card_number()
            safe_number = self.split_card_number(safe_number)
        return f'{self.name} {safe_number}'


    def get_safe_account(self):
        """возвращает номер счета в формате **XXXX (видны только последние 4 цифры номера счета)"""
        return '*'*2 + self.number[-4:]


    def get_safe_card_number(self):
        """Выводит номер счета в формате XXXX XX** **** XXXX (видны первые 6 цифр и последние 4, разбит по блокам по 4 цифры, разделенных пробелом)."""
        start, middle, end = self.number[:6], self.number[6:-4], self.number[-4:]
        return start + '*'*len(middle) + end


    @staticmethod
    def split_card_number(card_number):
        """Разбивает номер счета на блоки по 4 цифры"""
        return f'{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}'


class Amount:
    """Сумма перевода, валюта"""

    def __init__(self, value, currency_name, currency_code):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.value = value
        self.currency_name = currency_name
        self.currency_code = currency_code


    def __repr__(self):  # pragma: nocover
        return f'Amount(value={self.value}, currency_name={self.currency_name})'


class Operation:
    """Операция"""

    def __init__(self, id, state, date, amount, description, payment_from=None, payment_to=None):
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.id = id
        self.state = state
        self.date = date
        self.amount = amount
        self.description = description
        self.payment_from = payment_from
        self.payment_to = payment_to


    @classmethod
    def init_from_dict(cls, data):
        """Возващает инфо об операции из списка"""
        return cls(
            id=int(data['id']),
            state=data['state'],
            date=datetime.fromisoformat(data['date']),
            amount=Amount(
                value=float(data['operationAmount']['amount']),
                currency_name=data['operationAmount']['currency']['name'],
                currency_code=data['operationAmount']['currency']['code']
            ),
            description =data['description'],
            payment_to=Payment.init_from_str(data['to']),
            payment_from=Payment.init_from_str(data['from']) if 'from' in data else None
        )


    def safe(self):
        """
        Возвращает информацию о выполенной операции в формате:
        <дата перевода> <описание перевода>
        <откуда> -> <куда>
        <сумма перевода> <валюта>
        """
        lines = [
            f'{self.date.strftime("%d.%m.%Y")} {self.description}',
        ]
        if self.payment_from:
            lines.append(f'{self.payment_from.safe()} -> {self.payment_to.safe()}')
        else:
            lines.append(f'{self.payment_to.safe()}')
        lines.append(f'{self.amount.value:.2f} {self.amount.currency_name}')
        return '\n'.join(lines)


    def __repr__(self):  # pragma: nocover
        return (
            f'Operation('
        f'{self.id}, {self.description}, state={self.state}, date={self.date}, amount={self.amount}, from={self.payment_from}, to={self.payment_to}')