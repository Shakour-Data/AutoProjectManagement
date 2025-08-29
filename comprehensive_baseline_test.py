#!/usr/bin/env python3
"""
Comprehensive test suite for scope baseline management functionality.
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from autoprojectmanagement.main_modules.planning_estimation.scope_management import ScopeManagement

class ComprehensiveBaselineTest:
    """Comprehensive test class for baseline management functionality."""
    
    def __init__(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="scope_test_"))
        self.setup_test_environment()
    
    def setup_test_environment(self):
        """Set up test environment with comprehensive test data."""
        print(f"Setting up test environment in: {self.test_dir}")
        
        # Create test directories
        test_dirs = [
            'data/inputs/UserInputs',
            'data/inputs/OutPuts'
        ]
        
        for dir_path in test_dirs:
            (self.test_dir / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create comprehensive test WBS data
        test_wbs = {
            'id': 'project_root',
            'name': 'Comprehensive Test Project',
            'description': 'Test project for comprehensive baseline testing',
            'estimated_duration': 100,
            'resource_cost': 25000,
            'complexity': 'high',
            'subtasks': [
                {
                    'id': 'phase_1',
                    'name': 'Phase 1: Planning',
                    'description': 'Initial planning phase',
                    'estimated_duration': 20,
                    'resource_cost': 5000,
                    'subtasks': [
                        {
                            'id': 'task_1_1',
                            'name': 'Requirements Gathering',
                            'description': 'Gather project requirements',
                            'estimated_duration': 10,
                            'resource_cost': 2000,
                            'dependencies': []
                        },
                        {
                            'id': 'task_1_2',
                            'name': 'Architecture Design',
                            'description': 'Design system architecture',
                            'estimated_duration': 8,
                            'resource_cost': 2500,
                            'dependencies': ['task_1_1']
                        }
                    ]
                },
                {
                    'id': 'phase_2',
                    'name': 'Phase 2: Development',
                    'description': 'Development phase',
                    'estimated_duration': 60,
                    'resource_cost': 15000,
                    'subtasks': [
                        {
                            'id': 'task_2_1',
                            'name': 'Frontend Development',
                            'description': 'Develop frontend components',
                            'estimated_duration': 30,
                            'resource_cost': 8000,
                            'dependencies': ['task_1_2']
                        },
                        {
                            'id': 'task_2_2',
                            'name': 'Backend Development',
                            'description': 'Develop backend services',
                            'estimated_duration': 25,
                            'resource_cost': 6000,
                            'dependencies': ['task_1_2']
                        }
                    ]
                }
            ]
        }
        
        # Create test scope changes
        test_changes = [
            {
                'task_id': 'task_1_3',
                'change_type': 'add',
                'details': {
                    'parent_id': 'phase_1',
                    'task': {
                        'id': 'task_1_3',
                        'name': 'Risk Assessment',
                        'description': 'Assess project risks',
                        'estimated_duration': 5,
                        'resource_cost': 1000,
                        'dependencies': ['task_1_1']
                    }
                }
            },
            {
                'task_id': 'task_2_1',
                'change_type': 'modify',
                'details': {
                    'estimated_duration': 35,
                    'resource_cost': 9000,
                    'modification_complexity': 'medium'
                }
            }
        ]
        
        # Save test files
        with open(self.test_dir / 'data/inputs/UserInputs/detailed_wbs.json', 'w') as f:
            json.dump(test_wbs, f, indent=2)
        
        with open(self.test_dir / 'data/inputs/UserInputs/scope_changes.json', 'w') as f:
            json.dump(test_changes, f, indent=2)
        
        print("Comprehensive test environment setup complete")
    
    def create_manager(self):
        """Create a ScopeManagement instance with test paths."""
        return ScopeManagement(
            detailed_wbs_path=str(self.test_dir / 'data/inputs/UserInputs/detailed_wbs.json'),
            scope_changes_path=str(self.test_dir / 'data/inputs/UserInputs/scope_changes.json'),
            output_path=str(self.test_dir / 'data/inputs/OutPuts/scope_management.json')
        )
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        print("\n=== Testing Edge Cases ===")
        
        manager = self.create_manager()
        manager.load_inputs()
        
        test_results = []
        
        # Test 1: Invalid baseline name (empty string)
        try:
            result = manager.create_baseline("", "Empty name test")
            success = not result  # Should return False for invalid name
            print(f"Empty baseline name handled: {success}")
            test_results.append(success)
        except Exception as e:
            print(f"Empty baseline name exception: {e}")
            test_results.append(False)
        
        # Test 2: Non-existent baseline restoration
        try:
            result = manager.restore_baseline("non_existent_baseline")
            success = not result  # Should return False for non-existent baseline
            print(f"Non-existent baseline restoration handled: {success}")
            test_results.append(success)
        except Exception as e:
            print(f"Non-existent baseline exception: {e}")
            test_results.append(False)
        
        # Test 3: Non-existent baseline comparison
        try:
            result = manager.compare_with_baseline("non_existent_baseline")
            success = len(result.get('differences', [])) == 0  # Should return empty differences
            print(f"Non-existent baseline comparison handled: {success}")
            test_results.append(success)
        except Exception as e:
            print(f"Non-existent baseline comparison exception: {e}")
            test_results.append(False)
        
        # Test 4: Non-existent baseline deletion
        try:
            result = manager.delete_baseline("non_existent_baseline")
            success = not result  # Should return False for non-existent baseline
            print(f"Non-existent baseline deletion handled: {success}")
            test_results.append(success)
        except Exception as e:
            print(f"Non-existent baseline deletion exception: {e}")
            test_results.append(False)
        
        # Test 5: Missing baseline file
        baseline_path = self.test_dir / 'data/inputs/UserInputs/scope_baselines.json'
        if baseline_path.exists():
            baseline_path.unlink()
        
        try:
            result = manager.get_baseline_list()
            success = isinstance(result, list)  # Should return empty list
            print(f"Missing baseline file handled: {success}")
            test_results.append(success)
        except Exception as e:
            print(f"Missing baseline file exception: {e}")
            test_results.append(False)
        
        return all(test_results)
    
    def test_performance_large_wbs(self):
        """Test performance with large WBS structures."""
        print("\n=== Testing Performance with Large WBS ===")
        
        # Create a large WBS structure
        large_wbs = {
            'id': 'large_project',
            'name': 'Large Test Project',
            'description': 'Project with many tasks for performance testing',
            'estimated_duration': 500,
            'resource_cost': 100000,
            'subtasks': []
        }
        
        # Add 100 tasks
        for i in range(100):
            task = {
                'id': f'task_{i+1}',
                'name': f'Task {i+1}',
                'description': f'Test task {i+1}',
                'estimated_duration': i % 10 + 1,
                'resource_cost': (i % 10 + 1) * 100,
                'subtasks': []
            }
            large_wbs['subtasks'].append(task)
        
        # Save large WBS
        large_wbs_path = self.test_dir / 'data/inputs/UserInputs/large_wbs.json'
        with open(large_wbs_path, 'w') as f:
            json.dump(large_wbs, f, indent=2)
        
        # Test with large WBS
        manager = ScopeManagement(
            detailed_wbs_path=str(large_wbs_path),
            scope_changes_path=str(self.test_dir / 'data/inputs/UserInputs/scope_changes.json'),
            output_path=str(self.test_dir / 'data/inputs/OutPuts/large_scope_management.json')
        )
        
        manager.load_inputs()
        
        import time
        start_time = time.time()
        
        # Create baseline
        manager.create_baseline("large_baseline", "Baseline for large WBS")
        
        # Compare
        comparison = manager.compare_with_baseline("large_baseline")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Large WBS performance test completed in {duration:.3f} seconds")
        print(f"Comparison summary: {comparison['summary']}")
        
        return duration < 5.0  # Should complete in reasonable time
    
    def test_comprehensive_comparison(self):
        """Test comprehensive comparison functionality."""
        print("\n=== Testing Comprehensive Comparison ===")
        
        manager = self.create_manager()
        manager.load_inputs()
        
        # Create initial baseline
        manager.create_baseline("comprehensive_baseline", "Comprehensive test baseline")
        
        # Apply changes
        manager.apply_scope_changes()
        
        # Make additional modifications for testing
        task_2_1 = manager.find_task_by_id('task_2_1')
        if task_2_1:
            original_duration = task_2_1.get('estimated_duration', 0)
            task_2_1['estimated_duration'] = original_duration + 5
            task_2_1['resource_cost'] = task_2_1.get('resource_cost', 0) + 1000
        
        # Compare with comprehensive details
        comparison = manager.compare_with_baseline("comprehensive_baseline")
        
        print(f"Comprehensive comparison results:")
        print(f"  Tasks added: {comparison['summary']['tasks_added']}")
        print(f"  Tasks removed: {comparison['summary']['tasks_removed']}")
        print(f"  Tasks modified: {comparison['summary']['tasks_modified']}")
        print(f"  Changes applied: {comparison['summary']['changes_applied']}")
        
        # Show detailed differences
        print(f"\nDetailed differences ({len(comparison['differences'])} found):")
        for i, diff in enumerate(comparison['differences'][:10]):  # Show first 10
            print(f"  {i+1}. {diff['type']}: {diff.get('task_id', diff.get('field', 'unknown'))}")
        
        return len(comparison['differences']) > 0
    
    def test_integration_workflow(self):
        """Test integration with full scope management workflow."""
        print("\n=== Testing Integration Workflow ===")
        
        manager = self.create_manager()
        
        # Run complete workflow
        manager.run()
        
        # Check if output file was created
        output_path = self.test_dir / 'data/inputs/OutPuts/scope_management.json'
        if output_path.exists():
            with open(output_path, 'r') as f:
                output_data = json.load(f)
            
            print("Integration workflow completed successfully")
            print(f"Output contains: {len(output_data.get('scope_changes', []))} changes")
            print(f"Impact analyses: {len(output_data.get('impact_analyses', []))}")
            print(f"Approval results: {len(output_data.get('approval_results', []))}")
            
            return True
        else:
            print("Integration workflow failed - output file not found")
            return False
    
    def run_all_tests(self):
        """Run all comprehensive tests."""
        print("Starting Comprehensive Baseline Management Tests")
        print("=" * 60)
        
        test_results = {}
        
        try:
            test_results['edge_cases'] = self.test_edge_cases()
            test_results['performance'] = self.test_performance_large_wbs()
            test_results['comparison'] = self.test_comprehensive_comparison()
            test_results['integration'] = self.test_integration_workflow()
            
            print("\n" + "=" * 60)
            print("Comprehensive Test Results Summary:")
            for test_name, result in test_results.items():
                status = "PASS" if result else "FAIL"
                print(f"  {test_name}: {status}")
            
            all_passed = all(test_results.values())
            if all_passed:
                print("\nAll comprehensive tests completed successfully!")
            else:
                print("\nSome tests failed. Please review the output.")
            
            return all_passed
            
        except Exception as e:
            print(f"Comprehensive test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cleanup(self):
        """Clean up test environment."""
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            print(f"Cleaned up test directory: {self.test_dir}")

def main():
    """Main test function."""
    tester = ComprehensiveBaselineTest()
    
    try:
        success = tester.run_all_tests()
        return 0 if success else 1
    finally:
        tester.cleanup()

if __name__ == "__main__":
    sys.exit(main())
