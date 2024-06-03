import pytest


@pytest.fixture
def operation_data_with_from():
    return {
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
  },

@pytest.fixture
def operation_data_without_from(operation_data_with_from):
    operation_data_with_from['description'] = 'Открытие вклада'
    del operation_data_with_from['from']
    return operation_data_with_from
