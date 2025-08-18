# Comprehensive unit tests for resource management module
# This file contains comprehensive unit tests for the resource management module
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
# including task management, progress calculation, and resource_allocation
            end_date="2024-01-19"
        )
        
        expected_utilization = 30 / 32  # 93.75%
        assert abs(utilization - expected_utilization) < 0.01
    
    def test_prevent_overallocation(self, resource_manager, sample_resource_data):
        """Test preventing overallocation of resources"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        # Try to allocate more hours than available
        with pytest.raises(ValueError, match="Resource overallocation"):
            resource_manager.allocate_resource(
                resource.resource_id,
                "TASK-001",
                hours=50,  # More than 32 available hours
                start_date="2024-01-15",
                end_date="2024-01-19"
            )
    
    def test_update_resource_availability(self, resource_manager, sample_resource_data):
        """Test updating resource availability"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        updated_resource = resource_manager.update_resource(
            resource.resource_id,
            {"availability": 0.6}
        )
        
        assert updated_resource.availability == 0.6
    
    def test_get_resource_workload(self, resource_manager, sample_resource_data):
        """Test getting resource workload overview"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        # Allocate multiple tasks
        resource_manager.allocate_resource(
            resource.resource_id,
            "TASK-001",
            hours=16,
            start_date="2024-01-15",
            end_date="2024-01-17"
        )
        
        resource_manager.allocate_resource(
            resource.resource_id,
            "TASK-002",
            hours=8,
            start_date="2024-01-18",
            end_date="2024-01-19"
        )
        
        workload = resource_manager.get_resource_workload(resource.resource_id)
        assert workload["total_allocated_hours"] == 24
        assert len(workload["active_allocations"]) == 2
    
    def test_find_available_resources(self, resource_manager, sample_resource_data):
        """Test finding available resources for a task"""
        resource_manager.create_resource(sample_resource_data)
        
        # Create another resource with lower availability
        resource2_data = sample_resource_data.copy()
        resource2_data["resource_id"] = "RES-002"
        resource2_data["availability"] = 0.4
        resource_manager.create_resource(resource2_data)
        
        # Find resources available for 20 hours
        available_resources = resource_manager.find_available_resources(
            required_hours=20,
            required_skills=["Python"],
            start_date="2024-01-15",
            end_date="2024-01-19"
        )
        
        # Only RES-001 should be available (32 hours capacity)
        assert len(available_resources) == 1
        assert available_resources[0].resource_id == "RES-001"
    
    def test_get_resource_cost(self, resource_manager, sample_resource_data):
        """Test calculating resource cost for a task"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        cost = resource_manager.calculate_resource_cost(
            resource.resource_id,
            hours=16
        )
        
        expected_cost = 16 * 75.0  # 16 hours * $75/hour
        assert cost == expected_cost
    
    def test_resource_skill_matching_score(self, resource_manager, sample_resource_data):
        """Test calculating skill matching score"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        # Perfect match
        score1 = resource_manager.calculate_skill_match_score(
            resource.resource_id,
            required_skills=["Python", "Django"]
        )
        assert score1 == 1.0
        
        # Partial match
        score2 = resource_manager.calculate_skill_match_score(
            resource.resource_id,
            required_skills=["Python", "React"]
        )
        assert score2 == 0.5  # 2 out of 4 required skills match
    
    def test_delete_resource(self, resource_manager, sample_resource_data):
        """Test resource deletion"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        result = resource_manager.delete_resource(resource.resource_id)
        assert result is True
        
        with pytest.raises(ValueError, match="Resource not found"):
            resource_manager.get_resource(resource.resource_id)
    
    def test_get_resource_utilization_report(self, resource_manager, sample_resource_data):
        """Test generating resource utilization report"""
        resource = resource_manager.create_resource(sample_resource_data)
        
        # Allocate some work
        resource_manager.allocate_resource(
            resource.resource_id,
            "TASK-001",
            hours=24,
            start_date="2024-01-15",
            end_date="2024-01-19"
        )
        
        report = resource_manager.get_utilization_report(
            start_date="2024-01-15",
            end_date="2024-01-19"
        )
        
        assert resource.resource_id in report
        assert report[resource.resource_id]["utilization"] == 0.75  # 24/32
