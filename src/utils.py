import json
from cw3.src.dto import Operation, Amount, Payment
from cw3.src.config import operations


def get_operations(operations_json): #pragma: nocover
    """Загружает список операций из файла operations.json"""
    operations = []
    with open(operations_json, encoding='utf-8') as file:
        for data in json.load(file):
            if data:
                i = Operation.init_from_dict(data)
                operations.append(i)
    return operations


def filter_operations_by_state(*operations: Operation, state: str):
    """фильтрация списка операций по статусу"""
    filter_operations = []
    for i in operations:
        if i.state == state:
            filter_operations.append(i)
    return filter_operations


def sort_operation_by_date(*operations: Operation):
    """возвращает список, отсортированный по дате (сначала последние операции)"""
    return sorted(operations, key=lambda i: i.date, reverse= True)