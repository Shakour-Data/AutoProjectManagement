"""Risk management module for identifying, categorizing, and managing project risks.

This module provides comprehensive risk management capabilities including:
- Risk identification from GitHub issues
- Risk categorization by activity and WBS
- Project risk score calculation
- Risk mitigation strategies
"""

from typing import Dict, List, Any, Optional, Union
from collections import defaultdict
from autoprojectmanagement.services.github_integration import GitHubIntegration

# Constants for risk management
RISK_LABEL = 'risk'
ACTIVITY_LABEL_PREFIX = 'activity:'
WBS_LABEL_PREFIX = 'wbs:'
IMPORTANCE_LABEL_PREFIX = 'importance:'
PRIORITY_LABEL_PREFIX = 'priority:'

# Risk levels and their corresponding values
RISK_LEVELS = {
    'low': 1,
    'medium': 3,
    'high': 5
}

DEFAULT_IMPORTANCE = 1.0
DEFAULT_PRIORITY = 1.0
DEFAULT_PROBABILITY = 0.5


class RiskManagement:
    """Manages project risks through identification, categorization, and assessment."""
    
    def __init__(self, github_integration: GitHubIntegration) -> None:
        """Initialize RiskManagement with GitHub integration.
        
        Args:
            github_integration: GitHubIntegration instance for accessing GitHub issues
        """
        self.github: GitHubIntegration = github_integration
        self.risk_issues: List[Dict[str, Any]] = []
        self.project_risk_score: float = 0.0
        self.activity_risks: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.wbs_risks: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.wbs_hierarchy: Dict[str, str] = {}  # parent-child relationships in WBS
        self.activity_importance: Dict[str, float] = {}  # importance scores
        self.activity_priority: Dict[str, float] = {}  # priority scores

    def identify_risks(self) -> List[Dict[str, Any]]:
        """Identify risks from GitHub issues labeled as 'risk'.
        
        This method fetches all open GitHub issues and filters them to find
        those labeled as 'risk'. It then categorizes these risks and calculates
        the overall project risk score.
        
        Returns:
            List of dictionaries containing risk issues with their details.
            
        Example:
            >>> risks = risk_manager.identify_risks()
            >>> print(f"Found {len(risks)} risks")
        """
        # Fetch all open issues from GitHub
        issues = self.github.get_issues(state="open")
        
        # Filter issues that have 'risk' label (case-insensitive)
        self.risk_issues = [
            issue for issue in issues 
            if 'risk' in [label['name'].lower() for label in issue.get('labels', [])]
        ]
        
        # Categorize risks by activity and WBS
        self._categorize_risks()
        
        # Calculate overall project risk score
        self._calculate_project_risk_score()
        
        return self.risk_issues

    def _categorize_risks(self) -> None:
        """Categorize risks by activity and WBS based on issue labels.
        
        This private method processes each risk issue and categorizes it based on
        labels such as activity, WBS, importance, and priority. It populates
        the internal dictionaries for activity risks, WBS risks, and their
        associated importance/priority scores.
        
        The method looks for specific label patterns:
        - activity:<activity_name> - associates risk with specific activity
        - wbs:<wbs_name> - associates risk with specific WBS element
        - importance:<float> - sets importance score for the activity
        - priority:<float> - sets priority score for the activity
        
        Raises:
            ValueError: If importance or priority labels contain invalid float values
        """
        for issue in self.risk_issues:
            labels = [label['name'].lower() for label in issue.get('labels', [])]
            activity: Optional[str] = None
            wbs: Optional[str] = None
            importance: float = DEFAULT_IMPORTANCE
            priority: float = DEFAULT_PRIORITY
            
            # Process each label to extract categorization information
            for label in labels:
                if label.startswith(ACTIVITY_LABEL_PREFIX):
                    # Extract activity name from label
                    activity = label.split(ACTIVITY_LABEL_PREFIX)[1].strip()
                elif label.startswith(WBS_LABEL_PREFIX):
                    # Extract WBS name from label
                    wbs = label.split(WBS_LABEL_PREFIX)[1].strip()
                elif label.startswith(IMPORTANCE_LABEL_PREFIX):
                    # Extract importance score from label
                    try:
                        importance = float(label.split(IMPORTANCE_LABEL_PREFIX)[1].strip())
                    except ValueError:
                        # Use default if parsing fails
                        importance = DEFAULT_IMPORTANCE
                elif label.startswith(PRIORITY_LABEL_PREFIX):
                    # Extract priority score from label
                    try:
                        priority = float(label.split(PRIORITY_LABEL_PREFIX)[1].strip())
                    except ValueError:
                        # Use default if parsing fails
                        priority = DEFAULT_PRIORITY
            
            # Categorize by activity if found
            if activity:
                self.activity_risks[activity].append(issue)
                self.activity_importance[activity] = importance
                self.activity_priority[activity] = priority
            
            # Categorize by WBS if found
            if wbs:
                self.wbs_risks[wbs].append(issue)

    def _calculate_project_risk_score(self) -> None:
        """Calculate the overall project risk score.
        
        This method calculates a comprehensive risk score for the entire project
        by considering:
        - Number of risks per activity
        - Importance scores for each activity
        - Priority scores for each activity
        
        The score is calculated as: Σ(risks_count × importance × priority)
        
        The result is stored in self.project_risk_score.
        """
        score: float = 0.0
        
        # Calculate risk score for each activity
        for activity, issues in self.activity_risks.items():
            importance = self.activity_importance.get(activity, DEFAULT_IMPORTANCE)
            priority = self.activity_priority.get(activity, DEFAULT_PRIORITY)
            # Weight risk count by importance and priority
            score += len(issues) * importance * priority
        
        self.project_risk_score = score

    def get_risk_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of all identified risks.
        
        This method creates a structured summary containing:
        - Total number of risks identified
        - Overall project risk score
        - Risks categorized by activity
        - Risks categorized by WBS
        - Detailed information about each risk
        
        Returns:
            Dictionary containing comprehensive risk summary with the following structure:
            {
                "total_risks": int,
                "project_risk_score": float,
                "activity_risks": Dict[str, int],
                "wbs_risks": Dict[str, int],
                "risks": List[Dict[str, Any]]
            }
            
        Example:
            >>> summary = risk_manager.get_risk_summary()
            >>> print(f"Total risks: {summary['total_risks']}")
            >>> print(f"Risk score: {summary['project_risk_score']}")
        """
        summary: Dict[str, Any] = {
            "total_risks": len(self.risk_issues),
            "project_risk_score": self.project_risk_score,
            "activity_risks": {
                activity: len(issues) 
                for activity, issues in self.activity_risks.items()
            },
            "wbs_risks": {
                wbs: len(issues) 
                for wbs, issues in self.wbs_risks.items()
            },
            "risks": [
                {
                    "id": issue['number'],
                    "title": issue['title'],
                    "created_at": issue['created_at'],
                    "url": issue['html_url']
                }
                for issue in self.risk_issues
            ]
        }
        return summary


# Standalone functions for backward compatibility with tests
def identify_risks(project_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify risks from project data.
    
    This function provides backward compatibility for identifying risks
    from project data structures. It extracts risk information from
    task definitions within the project data.
    
    Args:
        project_data: Dictionary containing project information including tasks.
                     Expected structure: {'tasks': [{'id': str, 'name': str, 'risk': str}]}
    
    Returns:
        List of dictionaries containing identified risks with task_id, risk_level,
        and task_name.
        
    Raises:
        TypeError: If project_data is None, not a dict, or has invalid structure
        TypeError: If tasks is None or not a list
        
    Example:
        >>> project_data = {
        ...     'tasks': [
        ...         {'id': 'T1', 'name': 'Task 1', 'risk': 'high'},
        ...         {'id': 'T2', 'name': 'Task 2', 'risk': 'low'}
        ...     ]
        ... }
        >>> risks = identify_risks(project_data)
        >>> print(f"Found {len(risks)} risks")
    """
    if project_data is None:
        raise TypeError("project_data cannot be None")
    
    if not isinstance(project_data, dict):
        raise TypeError("project_data must be a dictionary")
    
    tasks = project_data.get('tasks', [])
    if tasks is None:
        raise TypeError("tasks cannot be None")
    
    if not isinstance(tasks, list):
        raise TypeError("tasks must be a list")
    
    risks: List[Dict[str, Any]] = []
    
    # Process each task to extract risk information
    for task in tasks:
        if not isinstance(task, dict):
            raise TypeError("Each task must be a dictionary")
        
        risk_level = task.get('risk', 'low')
        if risk_level is not None:
            risks.append({
                'task_id': task.get('id'),
                'risk_level': risk_level,
                'task_name': task.get('name', 'Unnamed Task')
            })
    
    return risks


def assess_risk_impact(risk: Dict[str, Any]) -> float:
    """Assess the impact of a risk based on its level and probability.
    
    This function calculates a quantitative risk impact score based on:
    - Risk level (low, medium, high)
    - Probability of occurrence (0.0 to 1.0)
    
    The impact is calculated as: base_impact × probability
    
    Args:
        risk: Dictionary containing risk information with keys:
              - 'level': str, one of 'low', 'medium', 'high'
              - 'probability': float, between 0.0 and 1.0
    
    Returns:
        Float representing the calculated risk impact score.
        
    Raises:
        TypeError: If risk is None or not a dictionary
        TypeError: If risk level is not a string
        TypeError: If probability is not a number
        ValueError: If probability is not between 0 and 1
        
    Example:
        >>> risk = {'level': 'high', 'probability': 0.8}
        >>> impact = assess_risk_impact(risk)
        >>> print(f"Risk impact: {impact}")
    """
    if risk is None:
        raise TypeError("risk cannot be None")
    
    if not isinstance(risk, dict):
        raise TypeError("risk must be a dictionary")
    
    level = risk.get('level', 'low')
    probability = risk.get('probability', DEFAULT_PROBABILITY)
    
    if level is None:
        raise TypeError("risk level cannot be None")
    
    if not isinstance(level, str):
        raise TypeError("risk level must be a string")
    
    if level.lower() not in RISK_LEVELS:
        # Allow empty strings and other values to use default 'low'
        level = 'low'
    
    if probability is None:
        raise TypeError("probability cannot be None")
    
    if not isinstance(probability, (int, float)):
        raise TypeError("probability must be a number")
    
    if probability < 0 or probability > 1:
        raise ValueError("probability must be between 0 and 1")
    
    # Calculate risk impact using predefined risk level values
    base_impact = RISK_LEVELS[level.lower()]
    impact = base_impact * probability
    
    return impact


def mitigate_risk(risk: Dict[str, Any]) -> bool:
    """Mitigate a risk using predefined strategies.
    
    This function provides a basic risk mitigation framework. In a production
    environment, this would implement specific mitigation strategies based on:
    - Risk type and category
    - Available resources
    - Project constraints
    - Timeline requirements
    
    Args:
        risk: Dictionary containing risk information to be mitigated
    
    Returns:
        bool: True if mitigation was successful, False otherwise
        
    Raises:
        TypeError: If risk is None or not a dictionary
        
    Note:
        This is a simplified implementation. In practice, mitigation strategies
        would be much more sophisticated and risk-specific.
        
    Example:
        >>> risk = {'id': 'R1', 'level': 'high', 'type': 'technical'}
        >>> success = mitigate_risk(risk)
        >>> print(f"Mitigation successful: {success}")
    """
    if risk is None:
        raise TypeError("risk cannot be None")
    
    if not isinstance(risk, dict):
        raise TypeError("risk must be a dictionary")
    
    # TODO: Implement sophisticated mitigation strategies
    # For now, return True as a placeholder for successful mitigation
    return True


if __name__ == "__main__":
    repo_owner = "your_org_or_username"
    repo_name = "ProjectManagement"
    github = GitHubIntegration(repo_owner, repo_name)
    risk_manager = RiskManagement(github)
    risks = risk_manager.identify_risks()
    print(f"Identified {len(risks)} risks:")
    for risk in risks:
        print(f"- [{risk['number']}] {risk['title']} ({risk['html_url']})")
    summary = risk_manager.get_risk_summary()
    print("\nRisk Summary:")
    print(summary)
