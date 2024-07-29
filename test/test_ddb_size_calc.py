from src.ddb_size_calc import (
    calculate_attribute_size_in_bytes,
    calculate_item_size_in_bytes,
)
import pytest

test_item_data = [
    ({"BOOL": True}, 1),
    ({"BOOL": False}, 1),
    ({"S": "test name"}, 9),
    ({"S": "shorter"}, 7),
]


@pytest.mark.parametrize("test_input,expected", test_item_data)
def test_calculate_attribute_size_in_bytes(test_input, expected):
    actual_val = calculate_attribute_size_in_bytes(test_input)
    assert expected == actual_val
