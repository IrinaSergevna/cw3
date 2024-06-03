import datetime
import pytest
from src.dto import Payment, Operation


def test_init_from_str():
    payment = Payment.init_from_str('Visa Classic 7699855375169288')
    assert payment.name == 'Visa Classic'
    assert payment.number == '7699855375169288'


def test_get_safe_account():
    payment = Payment(name='Счет', number='7699855375169288')
    assert payment.safe() == 'Счет **9288'


def test_get_safe_card_number():
    payment = Payment(name='MasterCard', number='1796816785869527')
    assert payment.safe() == 'MasterCard 1796 81** **** 9527'


def test_split_card_number():
    card_number = '1796816785869527'
    result = Payment.split_card_number(card_number)
    assert result == '1796 8167 8586 9527'


def test_init_from_dict():
    data = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  }

    i = Operation.init_from_dict(data)
    assert i.id == 441945886
    assert i.state == 'EXECUTED'
    assert i.date == datetime.datetime(2019, 8, 26, 10, 50, 58, 294041)
    assert i.amount.value == 31957.58
    assert i.amount.currency_name == 'руб.'
    assert i.amount.currency_code == 'RUB'
    assert i.description == 'Перевод организации'
    assert i.payment_to.name == 'Счет'
    assert i.payment_to.number == '64686473678894779589'
    assert i.payment_from.name == 'Maestro'
    assert i.payment_from.number == '1596837868705199'


def test_init_from_dict_without_from():
    data =  {
    "id": 587085106,
    "state": "EXECUTED",
    "date": "2018-03-23T10:45:06.972075",
    "operationAmount": {
      "amount": "48223.05",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 41421565395219882431"
  }

    i = Operation.init_from_dict(data)
    assert i.id == 587085106
    assert i.state == 'EXECUTED'
    assert i.date == datetime.datetime(2018, 3, 23, 10, 45, 6, 972075)
    assert i.amount.value == 48223.05
    assert i.amount.currency_name == 'руб.'
    assert i.amount.currency_code == 'RUB'
    assert i.description == 'Открытие вклада'
    assert i.payment_to.name == 'Счет'
    assert i.payment_to.number == '41421565395219882431'


def test_safe_payment_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '26.08.2019 Перевод организации\n'
        'Maestro 1596 83** **** 5199 -> Счет **9589\n'
        '31957.58 руб.'
    )
    assert operation.safe() == expected_result

def test_safe_payment_without_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '26.08.2019 Открытие вклада\n'
        'Счет **9589\n'
        '31957.58 руб.'
    )
    assert operation.safe() == expected_result