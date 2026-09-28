"""Validation functions."""


def validate_required(value: str, field_name: str) -> None:
    """Validate that a required field has a value."""

    if not value or not value.strip():
        raise ValueError(f"{field_name} is required.")

def validate_positive_integer(value: int, field_name: str) -> None:
    """Validate that a value is a positive integer."""

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")