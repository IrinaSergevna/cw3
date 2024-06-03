# import pytest
# from cw3.src.utils import filter_operations_by_state
# from cw3.src.dto import Operation
#
#
# @pytest.fixture
# def canceled_operation(operation_data_with_from):
#     operation = Operation.init_from_dict(operation_data_with_from)
#     operation.state = "CANCELED"
#     return operation
#
# @pytest.fixture
# def executed_operation(operation_data_with_from):
#     operation = Operation.init_from_dict(operation_data_with_from)
#     operation.state = "EXECUTED"
#     return operation
#
# def test_filter_operations_by_state(canceled_operation, executed_operation):
#     operations = canceled_operation, executed_operation
#     [op] = filter_operations_by_state(*operations, state="CANCELED")
#     assert op == canceled_operation
#     [op] = filter_operations_by_state(*operations, state="EXECUTED")
#     assert op == executed_operation