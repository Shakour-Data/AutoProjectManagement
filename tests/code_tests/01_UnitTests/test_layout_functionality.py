#!/usr/bin/env python3
"""
Test script to verify dashboard layout functionality.
This script tests the API endpoints for layout management.
"""

import json
import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, '/home/gravitywaves/GravityProject/AutoProjectManagement')

def test_layout_directory():
    """Test that the layout directory exists and is writable."""
    layouts_dir = Path("JSonDataBase/OutPuts/dashboard_layouts")
    
    print("Testing layout directory...")
    print(f"Layout directory: {layouts_dir.absolute()}")
    
    # Create directory if it doesn't exist
    layouts_dir.mkdir(parents=True, exist_ok=True)
    
    # Test if directory exists and is writable
    if layouts_dir.exists():
        print("✓ Layout directory exists")
        
        # Test write permission
        test_file = layouts_dir / "test_write.txt"
        try:
            test_file.write_text("test")
            test_file.unlink()
            print("✓ Layout directory is writable")
        except Exception as e:
            print(f"✗ Layout directory is not writable: {e}")
            return False
    else:
        print("✗ Layout directory does not exist")
        return False
    
    return True

def test_default_layout_creation():
    """Test that default layouts can be created."""
    from autoprojectmanagement.api.dashboard_endpoints import create_default_layout
    
    print("\nTesting default layout creation...")
    
    # Test standard layout
    standard_layout = create_default_layout("standard")
    print(f"✓ Standard layout created: {standard_layout['layout_type']}")
    widgets_list = [w['widget_id'] for w in standard_layout['widgets']]
    print(f"  Widgets: {widgets_list}")
    
    # Test minimal layout
    minimal_layout = create_default_layout("minimal")
    print(f"✓ Minimal layout created: {minimal_layout['layout_type']}")
    
    # Test custom layout
    custom_layout = create_default_layout("custom")
    print(f"✓ Custom layout created: {custom_layout['layout_type']}")
    
    return True

def test_layout_validation():
    """Test layout validation functionality."""
    from autoprojectmanagement.api.dashboard_endpoints import DashboardLayout, WidgetPosition
    
    print("\nTesting layout validation...")
    
    # Test valid layout
    try:
        valid_widgets = [
            {"widget_id": "health", "position": 0, "enabled": True, "settings": {}},
            {"widget_id": "progress", "position": 1, "enabled": True, "settings": {}}
        ]
        valid_layout = DashboardLayout(
            layout_type="test",
            widgets=valid_widgets,
            refresh_rate=3000,
            theme="light"
        )
        print("✓ Valid layout validation passed")
    except Exception as e:
        print(f"✗ Valid layout validation failed: {e}")
        return False
    
    # Test invalid widget
    try:
        invalid_widgets = [
            WidgetPosition(widget_id="invalid_widget", position=0, enabled=True)
        ]
        invalid_layout = DashboardLayout(
            layout_type="test",
            widgets=invalid_widgets,
            refresh_rate=3000,
            theme="light"
        )
        print("✗ Invalid widget validation should have failed")
        return False
    except ValueError as e:
        print(f"✓ Invalid widget validation correctly failed: {e}")
    
    # Test duplicate widgets
    try:
        duplicate_widgets = [
            WidgetPosition(widget_id="health", position=0, enabled=True),
            WidgetPosition(widget_id="health", position=1, enabled=True)
        ]
        duplicate_layout = DashboardLayout(
            layout_type="test",
            widgets=duplicate_widgets,
            refresh_rate=3000,
            theme="light"
        )
        print("✗ Duplicate widget validation should have failed")
        return False
    except ValueError as e:
        print(f"✓ Duplicate widget validation correctly failed: {e}")
    
    # Test refresh rate validation
    try:
        invalid_refresh_layout = DashboardLayout(
            layout_type="test",
            widgets=valid_widgets,
            refresh_rate=500,  # Too low
            theme="light"
        )
        print("✗ Invalid refresh rate validation should have failed")
        return False
    except ValueError as e:
        print(f"✓ Invalid refresh rate validation correctly failed: {e}")
    
    return True

def test_layout_save_load():
    """Test layout save and load functionality."""
    from autoprojectmanagement.api.dashboard_endpoints import save_layout_config, get_layout_config
    
    print("\nTesting layout save and load...")
    
    # Create test layout
    test_layout = {
        "layout_type": "test_layout",
        "widgets": [
            {"widget_id": "health", "position": 0, "enabled": True, "settings": {}},
            {"widget_id": "progress", "position": 1, "enabled": True, "settings": {}}
        ],
        "refresh_rate": 5000,
        "theme": "dark",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    
    try:
        # Save layout
        saved_layout = save_layout_config(test_layout)
        print("✓ Layout saved successfully")
        print(f"  Layout type: {saved_layout['layout_type']}")
        
        # Load layout
        loaded_layout = get_layout_config("test_layout")
        print("✓ Layout loaded successfully")
        print(f"  Layout type: {loaded_layout['layout_type']}")
        print(f"  Widget count: {len(loaded_layout['widgets'])}")
        
        # Verify loaded layout matches saved layout
        assert loaded_layout['layout_type'] == test_layout['layout_type']
        assert len(loaded_layout['widgets']) == len(test_layout['widgets'])
        print("✓ Layout data integrity verified")
        
    except Exception as e:
        print(f"✗ Layout save/load test failed: {e}")
        return False
    
    return True

def test_available_layouts():
    """Test available layouts functionality."""
    from autoprojectmanagement.api.dashboard_endpoints import get_available_layouts
    
    print("\nTesting available layouts...")
    
    try:
        layouts = get_available_layouts()
        print(f"✓ Available layouts: {layouts}")
        
        # Should at least include standard layout
        if "standard" in layouts:
            print("✓ Standard layout is available")
        else:
            print("✗ Standard layout should be available")
            return False
            
    except Exception as e:
        print(f"✗ Available layouts test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Testing Dashboard Layout Functionality")
    print("=" * 50)
    
    tests = [
        test_layout_directory,
        test_default_layout_creation,
        test_layout_validation,
        test_layout_save_load,
        test_available_layouts
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(tests) - sum(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! Layout functionality is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
