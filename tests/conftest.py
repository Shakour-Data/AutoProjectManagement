"""
Pytest configuration file for AutoProjectManagement tests.
This file contains fixtures and configuration for all tests.
"""

import warnings
import pytest

# Filter out Pydantic deprecation warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*Pydantic V1 style.*",
    module=r".*pydantic.*"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*PydanticDeprecatedSince20.*",
    module=r".*pydantic.*"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*The `dict` method is deprecated.*",
    module=r".*pydantic.*"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*Using extra keyword arguments on `Field`.*",
    module=r".*pydantic.*"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*Support for class-based `config`.*",
    module=r".*pydantic.*"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r".*`json_encoders` is deprecated.*",
    module=r".*pydantic.*"
)

# Global fixtures and configuration
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for all tests."""
    # Any global setup can go here
    yield
    # Any global teardown can go here
