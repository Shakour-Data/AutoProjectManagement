import pytest
from src.autoprojectmanagement.services.integration_services.json_data_linker import link_json_data

def test_link_json_data():
    # Test linking valid JSON data
    data1 = {"key": "value"}
    data2 = {"key": "value2"}
    result = link_json_data(data1, data2)
    assert result == {"key": ["value", "value2"]}

def test_link_json_data_malformed():
    # Test linking malformed JSON data
    data1 = {"key": "value"}
    data2 = "not a json"
    with pytest.raises(ValueError):
        link_json_data(data1, data2)

def test_link_json_data_large_datasets():
    # Test linking large datasets
    data1 = {f"key{i}": f"value{i}" for i in range(1000)}
    data2 = {f"key{i}": f"value2_{i}" for i in range(1000)}
    result = link_json_data(data1, data2)
    assert len(result) == 2000  # Expecting combined keys

# Additional tests for edge cases and integration can be added here
