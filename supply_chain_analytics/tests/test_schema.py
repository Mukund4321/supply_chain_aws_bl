import sys
import os
import pytest

# Add project root to path so we can import our modules from within the tests folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import ValidationError
from models.order_schema import Order

# A valid order dict that satisfies all field types and the qty > 0 validator
VALID_ORDER = {
    "order_id": "ORD-001",
    "warehouse": "WH-A",
    "region": "North",
    "product": "Laptop",
    "order_qty": 10,
    "order_date": "2024-01-15",
    "delivery_date": "2024-01-22",
    "delivery_time_days": 7.0,
    "status": "Delivered"
}

# Test that a fully valid order dict passes Pydantic validation without errors
def test_valid_order_passes():
    order = Order(**VALID_ORDER)
    # Check that the model stored the values correctly
    assert order.order_id == "ORD-001"
    assert order.order_qty == 10

# Test that optional fields (region, delivery_time_days) can be None
def test_optional_fields_can_be_none():
    data = VALID_ORDER.copy()
    data['region'] = None
    data['delivery_time_days'] = None
    # Should not raise — these fields are Optional in the schema
    order = Order(**data)
    assert order.region is None

# Test that order_qty = 0 triggers the @field_validator and raises ValidationError
def test_zero_qty_raises_validation_error():
    data = VALID_ORDER.copy()
    data['order_qty'] = 0
    # pytest.raises checks that the code inside the block raises the expected exception
    with pytest.raises(ValidationError):
        Order(**data)

# Test that a negative order_qty also fails validation
def test_negative_qty_raises_validation_error():
    data = VALID_ORDER.copy()
    data['order_qty'] = -5
    with pytest.raises(ValidationError):
        Order(**data)
