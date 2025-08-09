"""
Test runner for wiki services unit tests
This module runs all wiki-related service tests
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def run_wiki_tests():
    """Run all wiki services tests"""
    test_files = [
        "test_wiki_git_operations.py",
        "test_wiki_page_mapper.py", 
        "test_wiki_sync_service.py"
    ]
    
    test_dir = Path(__file__).parent
    
    results = []
    for test_file in test_files:
        test_path = test_dir / test_file
        if test_path.exists():
            print(f"Running {test_file}...")
            result = pytest.main([str(test_path), "-v"])
            results.append((test_file, result))
    
    return results

def run_all_wiki_tests_with_coverage():
    """Run all wiki tests with coverage report"""
    test_dir = Path(__file__).parent
    
    # Run tests with coverage
    args = [
        str(test_dir),
        "-v",
        "--cov=autoprojectmanagement.services.wiki_git_operations",
        "--cov=autoprojectmanagement.services.wiki_page_mapper", 
        "--cov=autoprojectmanagement.services.wiki_sync_service",
        "--cov-report=html",
        "--cov-report=term-missing"
    ]
    
    return pytest.main(args)

if __name__ == "__main__":
    print("Wiki Services Test Runner")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        result = run_all_wiki_tests_with_coverage()
    else:
        results = run_wiki_tests()
        
        print("\n" + "=" * 50)
        print("Test Results Summary:")
        for test_file, result in results:
            status = "PASSED" if result == 0 else "FAILED"
            print(f"{test_file}: {status}")
    
    print("\nTo run with coverage: python test_wiki_services_runner.py --coverage")
