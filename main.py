from cw3.src.utils import get_operations, filter_operations_by_state, sort_operation_by_date
from cw3.src.dto import Operation, Amount, Payment
from cw3.src.config import operations

def main(operations_json='operations.json'):

    """
    выводит на экран список из 5 последних выполненных клиентом операций в формате:
    <дата перевода> <описание перевода>
    <откуда> -> <куда>
    <сумма перевода> <валюта>
    Пример вывода для одной операции:
    14.10.2018 Перевод организации
    Visa Platinum 7000 79** **** 6361 -> Счет **9638
    82771.72 руб.
    """

    operations = get_operations(operations_json)
    operations = filter_operations_by_state(*operations, state='EXECUTED')
    operations = sort_operation_by_date(*operations)
    for i in operations[:5]:
        print(f"{i.safe()}\n")


if __name__ == '__main__':
    main()