from pydantic import BaseModel, field_validator
from typing import Optional

# Pydantic is a data validation library — it checks that each field has the
# correct type and value before we process it. This catches bad data early
# rather than letting it silently corrupt our analytics results.

class Order(BaseModel):
    # Each field name matches a column in the CSV
    # Pydantic will raise a ValidationError if types don't match
    order_id: str
    warehouse: str

    # Optional means the value can be None (null) — region has 5 missing rows
    region: Optional[str] = None

    product: str
    order_qty: int
    order_date: str           # Stored as string; converted to datetime in cleaning
    delivery_date: str

    # Optional float because delivery_time_days has 11 missing values
    delivery_time_days: Optional[float] = None

    status: str

    # @field_validator runs extra logic on top of the type check
    # We use it to enforce that no order can have zero or negative quantity
    @field_validator('order_qty')
    @classmethod
    def qty_must_be_positive(cls, v):
        # A supply chain order must always have at least 1 unit
        # Zero or negative quantities indicate a data entry error
        if v <= 0:
            raise ValueError('order_qty must be greater than 0')
        return v
