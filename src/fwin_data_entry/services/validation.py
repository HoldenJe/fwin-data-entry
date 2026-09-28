"""Validation functions."""


def validate_required(value: str, field_name: str) -> None:
    """Validate that a required field has a value."""

    if not value or not value.strip():
        raise ValueError(f"{field_name} is required.")