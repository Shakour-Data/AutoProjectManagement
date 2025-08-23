# Predefined weights for urgency features
URGENCY_FEATURE_WEIGHTS = {
    "deadline_proximity": 9.5,
    "next_activity_dependency": 8.0,
    "high_delay_risk": 7.5,
    "immediate_decision": 8.5,
    "stakeholder_pressure": 7.0,
    "limited_resource_time": 6.5,
    "competitive_advantage": 6.0,
    "critical_issue_fix": 9.0,
    "external_schedule_coordination": 5.5,
    "high_compensatory_cost": 6.5,
}

# Predefined weights for importance features
IMPORTANCE_FEATURE_WEIGHTS = {
    "dependency": 8.0,
    "critical_path": 9.0,
    "schedule_impact": 7.5,
    "cost_impact": 7.0,
    "key_objectives": 8.5,
    "risk_complexity": 6.5,
    "resource_rarity": 6.0,
    "stakeholder_priority": 7.0,
    "milestone_role": 7.5,
    "quality_impact": 8.0,
    "bottleneck_potential": 7.0,
    "reuse_frequency": 5.5,
}

def calculate_weights(features):
    """
    Calculate weights for the given features dictionary.
    Raises TypeError if input is not a dict or contains invalid types.
    Returns a dictionary of calculated weights.
    """
    if not isinstance(features, dict):
        raise TypeError("Input features must be a dictionary")

    weights = {}
    for key, value in features.items():
        if not isinstance(key, str):
            raise TypeError("Feature keys must be strings")
        if not (isinstance(value, (int, float)) and not isinstance(value, bool)):
            raise TypeError("Feature values must be int or float (not bool)")

        # Calculate weight based on predefined weights or default to value
        urgency_weight = URGENCY_FEATURE_WEIGHTS.get(key, 0)
        importance_weight = IMPORTANCE_FEATURE_WEIGHTS.get(key, 0)
        combined_weight = (urgency_weight + importance_weight) * value
        weights[key] = combined_weight

    return weights
