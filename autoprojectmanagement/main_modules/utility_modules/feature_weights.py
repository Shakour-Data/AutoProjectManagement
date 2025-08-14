"""
path: autoprojectmanagement/main_modules/utility_modules/feature_weights.py
File: feature_weights.py
Purpose: Feature weights calculation module for project management prioritization
Author: AutoProjectManagement Team
Version: 2.0.0
License: MIT
Description: Calculates weighted scores for project features based on urgency and importance criteria
"""

from typing import Dict, Union, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Phase 1: Structure & Standards - Type definitions and constants
class FeatureCategory(Enum):
    """Enumeration for feature categories."""
    URGENCY = "urgency"
    IMPORTANCE = "importance"
    CUSTOM = "custom"

@dataclass
class WeightConfig:
    """Configuration for weight calculation."""
    min_weight: float = 0.0
    max_weight: float = 10.0
    default_weight: float = 5.0
    scale_factor: float = 1.0

@dataclass
class FeatureWeight:
    """Represents a single feature weight."""
    name: str
    category: FeatureCategory
    base_weight: float
    description: str
    validation_rules: Optional[Dict[str, float]] = None

# Phase 2: Documentation - Comprehensive feature weights with descriptions
# Predefined weights for urgency features with detailed descriptions
URGENCY_FEATURE_WEIGHTS: Dict[str, FeatureWeight] = {
    "deadline_proximity": FeatureWeight(
        name="deadline_proximity",
        category=FeatureCategory.URGENCY,
        base_weight=9.5,
        description="Proximity to deadline - higher weight for closer deadlines"
    ),
    "next_activity_dependency": FeatureWeight(
        name="next_activity_dependency",
        category=FeatureCategory.URGENCY,
        base_weight=8.0,
        description="Dependency on next activity - critical for workflow continuity"
    ),
    "high_delay_risk": FeatureWeight(
        name="high_delay_risk",
        category=FeatureCategory.URGENCY,
        base_weight=7.5,
        description="High risk of delay if not addressed immediately"
    ),
    "immediate_decision": FeatureWeight(
        name="immediate_decision",
        category=FeatureCategory.URGENCY,
        base_weight=8.5,
        description="Requires immediate decision or action"
    ),
    "stakeholder_pressure": FeatureWeight(
        name="stakeholder_pressure",
        category=FeatureCategory.URGENCY,
        base_weight=7.0,
        description="External pressure from stakeholders or clients"
    ),
    "limited_resource_time": FeatureWeight(
        name="limited_resource_time",
        category=FeatureCategory.URGENCY,
        base_weight=6.5,
        description="Limited time window for resource availability"
    ),
    "competitive_advantage": FeatureWeight(
        name="competitive_advantage",
        category=FeatureCategory.URGENCY,
        base_weight=6.0,
        description="Time-sensitive competitive advantage opportunity"
    ),
    "critical_issue_fix": FeatureWeight(
        name="critical_issue_fix",
        category=FeatureCategory.URGENCY,
        base_weight=9.0,
        description="Critical bug or issue requiring immediate fix"
    ),
    "external_schedule_coordination": FeatureWeight(
        name="external_schedule_coordination",
        category=FeatureCategory.URGENCY,
        base_weight=5.5,
        description="Coordination with external schedules or dependencies"
    ),
    "high_compensatory_cost": FeatureWeight(
        name="high_compensatory_cost",
        category=FeatureCategory.URGENCY,
        base_weight=6.5,
        description="High cost of delay or compensation required"
    ),
}

# Predefined weights for importance features with detailed descriptions
IMPORTANCE_FEATURE_WEIGHTS: Dict[str, FeatureWeight] = {
    "dependency": FeatureWeight(
        name="dependency",
        category=FeatureCategory.IMPORTANCE,
        base_weight=8.0,
        description="Number and criticality of dependencies"
    ),
    "critical_path": FeatureWeight(
        name="critical_path",
        category=FeatureCategory.IMPORTANCE,
        base_weight=9.0,
        description="Position on project critical path"
    ),
    "schedule_impact": FeatureWeight(
        name="schedule_impact",
        category=FeatureCategory.IMPORTANCE,
        base_weight=7.5,
        description="Impact on overall project schedule"
    ),
    "cost_impact": FeatureWeight(
        name="cost_impact",
        category=FeatureCategory.IMPORTANCE,
        base_weight=7.0,
        description="Financial impact on project budget"
    ),
    "key_objectives": FeatureWeight(
        name="key_objectives",
        category=FeatureCategory.IMPORTANCE,
        base_weight=8.5,
        description="Alignment with key project objectives"
    ),
    "risk_complexity": FeatureWeight(
        name="risk_complexity",
        category=FeatureCategory.IMPORTANCE,
        base_weight=6.5,
        description="Complexity and associated risk level"
    ),
    "resource_rarity": FeatureWeight(
        name="resource_rarity",
        category=FeatureCategory.IMPORTANCE,
        base_weight=6.0,
        description="Rarity or specialized nature of required resources"
    ),
    "stakeholder_priority": FeatureWeight(
        name="stakeholder_priority",
        category=FeatureCategory.IMPORTANCE,
        base_weight=7.0,
        description="Priority level assigned by stakeholders"
    ),
    "milestone_role": FeatureWeight(
        name="milestone_role",
        category=FeatureCategory.IMPORTANCE,
        base_weight=7.5,
        description="Role in achieving project milestones"
    ),
    "quality_impact": FeatureWeight(
        name="quality_impact",
        category=FeatureCategory.IMPORTANCE,
        base_weight=8.0,
        description="Impact on final deliverable quality"
    ),
    "bottleneck_potential": FeatureWeight(
        name="bottleneck_potential",
        category=FeatureCategory.IMPORTANCE,
        base_weight=7.0,
        description="Potential to become project bottleneck"
    ),
    "reuse_frequency": FeatureWeight(
        name="reuse_frequency",
        category=FeatureCategory.IMPORTANCE,
        base_weight=5.5,
        description="Frequency of reuse or applicability"
    ),
}

# Phase 3: Code Quality - Enhanced calculation logic with error handling
class FeatureWeightCalculator:
    """Advanced feature weight calculator with validation and error handling."""
    
    def __init__(self, config: Optional[WeightConfig] = None):
        """
        Initialize the calculator with configuration.
        
        Args:
            config: Weight configuration parameters
        """
        self.config = config or WeightConfig()
        self._validate_configuration()
        
    def _validate_configuration(self) -> None:
        """Validate the weight configuration."""
        if self.config.min_weight >= self.config.max_weight:
            raise ValueError("min_weight must be less than max_weight")
        if self.config.scale_factor <= 0:
            raise ValueError("scale_factor must be positive")
            
    def calculate_weights(
        self, 
        features: Dict[str, Union[int, float]], 
        category: Optional[FeatureCategory] = None
    ) -> Dict[str, float]:
        """
        Calculate weighted scores for given features.
        
        Args:
            features: Dictionary of feature names to values
            category: Optional category filter for features
            
        Returns:
            Dictionary of feature names to calculated weights
            
        Raises:
            TypeError: If features is not a dictionary
            ValueError: If feature values are invalid
        """
        if not isinstance(features, dict):
            raise TypeError("Features must be provided as a dictionary")
            
        if not features:
            logger.warning("Empty features dictionary provided")
            return {}
            
        weights = {}
        weight_sources = self._get_weight_sources(category)
        
        for feature_name, value in features.items():
            self._validate_feature_value(feature_name, value)
            weight = self._calculate_single_weight(
                feature_name, value, weight_sources
            )
            weights[feature_name] = weight
            
        logger.info(f"Calculated weights for {len(weights)} features")
        return weights
        
    def _get_weight_sources(
        self, 
        category: Optional[FeatureCategory]
    ) -> Dict[str, FeatureWeight]:
        """Get appropriate weight sources based on category."""
        if category == FeatureCategory.URGENCY:
            return URGENCY_FEATURE_WEIGHTS
        elif category == FeatureCategory.IMPORTANCE:
            return IMPORTANCE_FEATURE_WEIGHTS
        else:
            return {**URGENCY_FEATURE_WEIGHTS, **IMPORTANCE_FEATURE_WEIGHTS}
            
    def _validate_feature_value(
        self, 
        name: str, 
        value: Union[int, float]
    ) -> None:
        """Validate a single feature value."""
        if not isinstance(name, str):
            raise TypeError(f"Feature name must be string, got {type(name)}")
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Feature value must be numeric, got {type(value)} for {name}"
            )
        if not (self.config.min_weight <= value <= self.config.max_weight):
            raise ValueError(
                f"Feature value {value} for {name} is out of range "
                f"[{self.config.min_weight}, {self.config.max_weight}]"
            )
            
    def _calculate_single_weight(
        self,
        feature_name: str,
        value: Union[int, float],
        weight_sources: Dict[str, FeatureWeight]
    ) -> float:
        """Calculate weight for a single feature."""
        feature_weight = weight_sources.get(feature_name)
        if feature_weight:
            base_weight = feature_weight.base_weight
        else:
            logger.warning(f"Unknown feature: {feature_name}, using default")
            base_weight = self.config.default_weight
            
        normalized_value = value / self.config.max_weight
        calculated_weight = base_weight * normalized_value * self.config.scale_factor
        
        return round(calculated_weight, 2)
        
    def get_feature_info(self, feature_name: str) -> Optional[FeatureWeight]:
        """
        Get information about a specific feature.
        
        Args:
            feature_name: Name of the feature
            
        Returns:
            FeatureWeight object or None if not found
        """
        return (
            URGENCY_FEATURE_WEIGHTS.get(feature_name) or
            IMPORTANCE_FEATURE_WEIGHTS.get(feature_name)
        )
        
    def list_all_features(self) -> List[Tuple[str, FeatureWeight]]:
        """List all available features with their weights."""
        all_features = []
        all_features.extend(
            (name, weight) for name, weight in URGENCY_FEATURE_WEIGHTS.items()
        )
        all_features.extend(
            (name, weight) for name, weight in IMPORTANCE_FEATURE_WEIGHTS.items()
        )
        return all_features

# Phase 4: Integration - Backward compatibility and utility functions
def calculate_weights(features: Dict[str, Union[int, float]]) -> Dict[str, float]:
    """
    Legacy function for backward compatibility.
    
    Args:
        features: Dictionary of feature names to values
        
    Returns:
        Dictionary of calculated weights
        
    Example:
        >>> features = {"deadline_proximity": 8.5, "critical_path": 9.0}
        >>> weights = calculate_weights(features)
        >>> print(weights)
        {'deadline_proximity': 8.08, 'critical_path': 8.1}
    """
    calculator = FeatureWeightCalculator()
    return calculator.calculate_weights(features)

# Utility functions for integration
def validate_features(features: Dict[str, Union[int, float]]) -> bool:
    """
    Validate feature dictionary format.
    
    Args:
        features: Features dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        calculator = FeatureWeightCalculator()
        calculator.calculate_weights(features)
        return True
    except (TypeError, ValueError):
        return False

def get_weight_summary(features: Dict[str, Union[int, float]]) -> Dict[str, any]:
    """
    Get comprehensive weight summary for features.
    
    Args:
        features: Features dictionary
        
    Returns:
        Summary dictionary with weights and metadata
    """
    calculator = FeatureWeightCalculator()
    weights = calculator.calculate_weights(features)
    
    total_weight = sum(weights.values())
    max_feature = max(weights.items(), key=lambda x: x[1]) if weights else None
    min_feature = min(weights.items(), key=lambda x: x[1]) if weights else None
    
    return {
        "weights": weights,
        "total_weight": round(total_weight, 2),
        "max_feature": max_feature,
        "min_feature": min_feature,
        "feature_count": len(weights),
        "timestamp": datetime.now().isoformat()
    }

# Export public API
__all__ = [
    "FeatureWeightCalculator",
    "FeatureWeight",
    "FeatureCategory",
    "WeightConfig",
    "URGENCY_FEATURE_WEIGHTS",
    "IMPORTANCE_FEATURE_WEIGHTS",
    "calculate_weights",
    "validate_features",
    "get_weight_summary"
]
