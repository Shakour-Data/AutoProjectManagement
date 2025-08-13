"""
Risk Management Module for AutoProjectManagement.

This module provides comprehensive risk identification, assessment, and mitigation
capabilities for project management. It integrates with GitHub to identify risks
from issues and provides detailed risk analysis and reporting.

Classes:
    RiskManagement: Main class for managing project risks

Functions:
    identify_risks: Standalone function for risk identification
    assess_risk_impact: Assess the impact of individual risks
    mitigate_risk: Mitigate identified risks

Example:
    >>> from autoprojectmanagement.main_modules.communication_risk.risk_management import RiskManagement
    >>> from autoprojectmanagement.services.github_integration import GitHubIntegration
    >>> github = GitHubIntegration("owner", "repo")
    >>> risk_manager = RiskManagement(github)
    >>> risks = risk_manager.identify_risks()
    >>> summary = risk_manager.get_risk_summary()
    >>> print(f"Total risks: {summary['total_risks']}")
"""

import logging
from typing import Dict, List, Any, Optional, Union, DefaultDict
from collections import defaultdict
from autoprojectmanagement.services.github_integration import GitHubIntegration

# Constants
DEFAULT_IMPORTANCE = 1.0
DEFAULT_PRIORITY = 1.0
RISK_LABEL = 'risk'
MAX_LINE_LENGTH = 79
LEVEL_VALUES = {
    'low': 1,
    'medium': 3,
from typing import Dict, List, Any, Optional, Union, DefaultDict
from collections import defaultdict
from datetime import datetime

from autoprojectmanagement.services.github_integration import GitHubIntegration

# Constants
DEFAULT_IMPORTANCE = 1.0
DEFAULT_PRIORITY = 1.0
RISK_LEVELS = {'low', 'medium', 'high'}
LEVEL_VALUES = {'low': 1, 'medium': 3, 'high': 5}
MAX_LINE_LENGTH = 79

# Configure logging
logger = logging.getLogger(__name__)


class RiskManagement:
    """
    Main class for managing project risks through GitHub integration.

    This class provides methods to identify, categorize, and assess risks
    from GitHub issues. It calculates risk scores and provides comprehensive
    risk summaries.

    Attributes:
        github: GitHubIntegration instance for API interactions
        risk_issues: List of GitHub issues identified as risks
        project_risk_score: Overall project risk score
        activity_risks: Dictionary mapping activities to their risks
        wbs_risks: Dictionary mapping WBS elements to their risks
        wbs_hierarchy: Dictionary storing WBS parent-child relationships
        activity_importance: Dictionary mapping activities to importance scores
        activity_priority: Dictionary mapping activities to priority scores

    Example:
        >>> github = GitHubIntegration("owner", "repo")
        >>> risk_manager = RiskManagement(github)
        >>> risks = risk_manager.identify_risks()
        >>> summary = risk_manager.get_risk_summary()
    """

    def __init__(self, github_integration: GitHubIntegration) -> None:
        """
        Initialize RiskManagement with GitHub integration.

        Args:
            github_integration: GitHubIntegration instance for API access
        """
        self.github: GitHubIntegration = github_integration
        self.risk_issues: List[Dict[str, Any]] = []
        self.project_risk_score: float = 0.0
        self.activity_risks: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.wbs_risks: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.wbs_hierarchy: Dict[str, str] = {}
        self.activity_importance: Dict[str, float] = {}
        self.activity_priority: Dict[str, float] = {}

    def identify_risks(self) -> List[Dict[str, Any]]:
        """
        Identify risks from GitHub issues labeled as 'risk'.

        This method fetches open issues from GitHub and filters them
        to identify issues labeled as risks. It then categorizes these
        risks and calculates the overall project risk score.

        Returns:
            List of GitHub issues identified as risks

        Example:
            >>> risks = risk_manager.identify_risks()
            >>> print(f"Found {len(risks)} risks")
        """
        try:
            # Fetch open issues from GitHub
            issues = self.github.get_issues(state="open")
            
            # Filter issues with 'risk' label
            self.risk_issues = [
                issue for issue in issues
                if 'risk' in [
                    label['name'].lower() 
                    for label in issue.get('labels', [])
                ]
            ]
            
            # Categorize and score risks
            self._categorize_risks()
            self._calculate_project_risk_score()
            
            logger.info(f"Identified {len(self.risk_issues)} risks")
            return self.risk_issues
            
        except Exception as e:
            logger.error(f"Error identifying risks: {e}")
            raise

    def _categorize_risks(self) -> None:
        """
        Categorize risks by activity and WBS based on issue metadata.

        This private method processes each risk issue to extract
        activity, WBS, importance, and priority information from labels.
        It populates the internal dictionaries for risk categorization.
        """
        for issue in self.risk_issues:
            labels = [
                label['name'].lower() 
                for label in issue.get('labels', [])
            ]
            
            activity: Optional[str] = None
            wbs: Optional[str] = None
            importance: float = DEFAULT_IMPORTANCE
            priority: float = DEFAULT_PRIORITY
            
            # Parse labels for risk categorization
            for label in labels:
                if label.startswith("activity:"):
                    activity = label.split("activity:")[1].strip()
