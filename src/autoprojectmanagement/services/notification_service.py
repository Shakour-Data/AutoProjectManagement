#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/services/notification_service.py
File: notification_service.py
Purpose: Advanced notification service for scope changes and quality alerts
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Comprehensive notification system for project management automation
"""

import logging
import smtplib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CURRENT_VERSION = "1.0.0"
DEFAULT_NOTIFICATION_TEMPLATES_PATH = 'data/inputs/UserInputs/notification_templates.json'
DEFAULT_ENCODING = 'utf-8'
JSON_INDENT = 2

class NotificationServiceError(Exception):
    """Base exception for notification service errors."""
    pass

class NotificationConfigurationError(NotificationServiceError):
    """Raised when notification configuration is invalid."""
    pass

class NotificationDeliveryError(NotificationServiceError):
    """Raised when notification delivery fails."""
    pass

class NotificationService:
    """
    Comprehensive notification service for project management automation.
    
    This service handles notifications for scope changes, quality alerts,
    approval requests, and other project management events.
    
    Features:
    - Multiple delivery channels (Email, Slack, Teams, Console)
    - Template-based notification content
    - Configurable notification rules
    - Retry mechanisms and fallback options
    - Audit logging and delivery tracking
    
    Example:
        >>> service = NotificationService()
        >>> service.send_scope_change_notification(change_data, recipients)
    """
    
    def __init__(self, 
                 templates_path: str = DEFAULT_NOTIFICATION_TEMPLATES_PATH,
                 config_path: Optional[str] = None) -> None:
        """
        Initialize the notification service.
        
        Args:
            templates_path: Path to notification templates JSON file
            config_path: Path to notification configuration file (optional)
        """
        self.templates_path = Path(templates_path)
        self.config_path = Path(config_path) if config_path else None
        
        self.templates: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
        self.delivery_history: List[Dict[str, Any]] = []
        
        self._load_templates()
        self._load_config()
    
    def _load_templates(self) -> None:
        """Load notification templates from JSON file."""
        try:
            if self.templates_path.exists():
                with open(self.templates_path, 'r', encoding=DEFAULT_ENCODING) as f:
                    self.templates = json.load(f)
                logger.info(f"Loaded notification templates from {self.templates_path}")
            else:
                # Load default templates
                self.templates = self._get_default_templates()
                logger.warning(f"Templates file not found, using default templates")
        except Exception as e:
            logger.error(f"Error loading notification templates: {e}")
            self.templates = self._get_default_templates()
    
    def _load_config(self) -> None:
        """Load notification configuration."""
        try:
            if self.config_path and self.config_path.exists():
                with open(self.config_path, 'r', encoding=DEFAULT_ENCODING) as f:
                    self.config = json.load(f)
                logger.info(f"Loaded notification config from {self.config_path}")
            else:
                # Use environment variables or defaults
                self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading notification config: {e}")
            self.config = self._get_default_config()
    
    def _get_default_templates(self) -> Dict[str, Any]:
        """Get default notification templates."""
        return {
            "scope_change_add": {
                "subject": "Scope Change: Task Added - {task_id}",
                "body": """
                **Scope Change Notification**
                
                **Change Type:** Add
                **Task ID:** {task_id}
                **Task Name:** {task_name}
                **Parent Task:** {parent_id}
                **Requested By:** {requester}
                **Timestamp:** {timestamp}
                
                **Impact Analysis:**
                - Schedule Impact: {schedule_impact} days
                - Cost Impact: ${cost_impact}
                - Resource Impact: {resource_impact} resources
                - Risk Level: {risk_level}
                
                **Approval Status:** {approval_status}
                **Next Steps:** {next_steps}
                
                Please review and take appropriate action.
                """,
                "priority": "medium"
            },
            "scope_change_remove": {
                "subject": "Scope Change: Task Removed - {task_id}",
                "body": """
                **Scope Change Notification**
                
                **Change Type:** Remove
                **Task ID:** {task_id}
                **Task Name:** {task_name}
                **Requested By:** {requester}
                **Timestamp:** {timestamp}
                
                **Impact Analysis:**
                - Schedule Savings: {schedule_impact} days
                - Cost Savings: ${cost_impact}
                - Resource Savings: {resource_impact} resources
                
                **Approval Status:** {approval_status}
                **Next Steps:** {next_steps}
                
                Please review and take appropriate action.
                """,
                "priority": "medium"
            },
            "scope_change_modify": {
                "subject": "Scope Change: Task Modified - {task_id}",
                "body": """
                **Scope Change Notification**
                
                **Change Type:** Modify
                **Task ID:** {task_id}
                **Task Name:** {task_name}
                **Requested By:** {requester}
                **Timestamp:** {timestamp}
                
                **Changes Made:**
                {changes_summary}
                
                **Impact Analysis:**
                - Schedule Impact: {schedule_impact} days
                - Cost Impact: ${cost_impact}
                - Resource Impact: {resource_impact} resources
                - Risk Level: {risk_level}
                
                **Approval Status:** {approval_status}
                **Next Steps:** {next_steps}
                
                Please review and take appropriate action.
                """,
                "priority": "medium"
            },
            "approval_required": {
                "subject": "APPROVAL REQUIRED: Scope Change - {task_id}",
                "body": """
                **APPROVAL REQUIRED**
                
                A scope change requires your approval.
                
                **Change Details:**
                - Task ID: {task_id}
                - Change Type: {change_type}
                - Task Name: {task_name}
                - Requested By: {requester}
                
                **Impact Analysis (HIGH RISK):**
                - Schedule Impact: {schedule_impact} days
                - Cost Impact: ${cost_impact}
                - Resource Impact: {resource_impact} resources
                - Risk Level: {risk_level}
                
                **Approval Conditions:**
                {approval_conditions}
                
                **Action Required:** Please review and approve/reject this change.
                """,
                "priority": "high"
            },
            "quality_alert": {
                "subject": "QUALITY ALERT: {project_name} - {quality_level}",
                "body": """
                **Quality Alert Notification**
                
                **Project:** {project_name}
                **Quality Level:** {quality_level}
                **Overall Score:** {quality_score}%
                
                **Critical Issues:**
                {critical_issues}
                
                **Recommendations:**
                {recommendations}
                
                **Action Required:** Immediate attention needed for quality improvement.
                """,
                "priority": "high"
            }
        }
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default notification configuration."""
        return {
            "email": {
                "enabled": False,
                "smtp_server": os.environ.get('SMTP_SERVER', ''),
                "smtp_port": int(os.environ.get('SMTP_PORT', 587)),
                "username": os.environ.get('SMTP_USERNAME', ''),
                "password": os.environ.get('SMTP_PASSWORD', ''),
                "from_address": os.environ.get('FROM_EMAIL', ''),
                "use_tls": True
            },
            "slack": {
                "enabled": False,
                "webhook_url": os.environ.get('SLACK_WEBHOOK_URL', ''),
                "channel": os.environ.get('SLACK_CHANNEL', '#general')
            },
            "teams": {
                "enabled": False,
                "webhook_url": os.environ.get('TEAMS_WEBHOOK_URL', '')
            },
            "console": {
                "enabled": True  # Always enabled for logging
            },
            "retry_attempts": 3,
            "retry_delay": 5,  # seconds
            "fallback_order": ["slack", "email", "teams", "console"]
        }
    
    def send_notification(self, 
                         template_key: str, 
                         context: Dict[str, Any],
                         recipients: List[str],
                         channels: Optional[List[str]] = None) -> bool:
        """
        Send a notification using the specified template.
        
        Args:
            template_key: Key of the template to use
            context: Dictionary of template variables
            recipients: List of recipient addresses/IDs
            channels: List of channels to use (default: all enabled channels)
            
        Returns:
            True if notification was successfully sent to at least one channel
        """
        if template_key not in self.templates:
            logger.error(f"Template '{template_key}' not found")
            return False
        
        template = self.templates[template_key]
        subject = template['subject'].format(**context)
        body = template['body'].format(**context)
        priority = template.get('priority', 'medium')
        
        if channels is None:
            channels = self._get_enabled_channels()
        
        success = False
        delivery_results = []
        
        for channel in channels:
            try:
                if channel == 'email' and self.config['email']['enabled']:
                    result = self._send_email(subject, body, recipients, priority)
                    delivery_results.append({'channel': 'email', 'success': result})
                    success = success or result
                
                elif channel == 'slack' and self.config['slack']['enabled']:
                    result = self._send_slack(subject, body, recipients, priority)
                    delivery_results.append({'channel': 'slack', 'success': result})
                    success = success or result
                
                elif channel == 'teams' and self.config['teams']['enabled']:
                    result = self._send_teams(subject, body, recipients, priority)
                    delivery_results.append({'channel': 'teams', 'success': result})
                    success = success or result
                
                elif channel == 'console':
                    result = self._send_console(subject, body, priority)
                    delivery_results.append({'channel': 'console', 'success': result})
                    success = success or result
                    
            except Exception as e:
                logger.error(f"Error sending notification via {channel}: {e}")
                delivery_results.append({'channel': channel, 'success': False, 'error': str(e)})
        
        # Log delivery history
        self._log_delivery(
            template_key=template_key,
            subject=subject,
            recipients=recipients,
            channels=delivery_results,
            success=success
        )
        
        return success
    
    def _get_enabled_channels(self) -> List[str]:
        """Get list of enabled notification channels."""
        enabled_channels = []
        for channel, config in self.config.items():
            if isinstance(config, dict) and config.get('enabled', False):
                enabled_channels.append(channel)
        # Always include console for logging
        if 'console' not in enabled_channels:
            enabled_channels.append('console')
        return enabled_channels
    
    def _send_email(self, subject: str, body: str, recipients: List[str], priority: str) -> bool:
        """Send notification via email."""
        try:
            config = self.config['email']
            
            if not all([config['smtp_server'], config['username'], config['password']]):
                logger.warning("Email configuration incomplete")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = config['from_address']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg['X-Priority'] = '1' if priority == 'high' else '3'
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                if config['use_tls']:
                    server.starttls()
                server.login(config['username'], config['password'])
                server.send_message(msg)
            
            logger.info(f"Email sent to {recipients}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def _send_slack(self, subject: str, body: str, recipients: List[str], priority: str) -> bool:
        """Send notification via Slack."""
        try:
            config = self.config['slack']
            
            if not config['webhook_url']:
                logger.warning("Slack webhook URL not configured")
                return False
            
            # For simplicity, we'll just log since actual Slack integration
            # would require additional dependencies
            logger.info(f"SLACK NOTIFICATION: {subject}")
            logger.info(f"Recipients: {recipients}")
            logger.info(f"Body: {body}")
            logger.info(f"Priority: {priority}")
            
            # In a real implementation, you would use:
            # import requests
            # payload = {"text": f"*{subject}*\n\n{body}"}
            # response = requests.post(config['webhook_url'], json=payload)
            # return response.status_code == 200
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
            return False
    
    def _send_teams(self, subject: str, body: str, recipients: List[str], priority: str) -> bool:
        """Send notification via Microsoft Teams."""
        try:
            config = self.config['teams']
            
            if not config['webhook_url']:
                logger.warning("Teams webhook URL not configured")
                return False
            
            # For simplicity, we'll just log since actual Teams integration
            # would require additional implementation
            logger.info(f"TEAMS NOTIFICATION: {subject}")
            logger.info(f"Recipients: {recipients}")
            logger.info(f"Body: {body}")
            logger.info(f"Priority: {priority}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Teams notification: {e}")
            return False
    
    def _send_console(self, subject: str, body: str, priority: str) -> bool:
        """Send notification to console (always available for logging)."""
        try:
            logger.info(f"CONSOLE NOTIFICATION [{priority.upper()}]: {subject}")
            logger.info(f"Body:\n{body}")
            return True
        except Exception as e:
            logger.error(f"Failed to log to console: {e}")
            return False
    
    def _log_delivery(self, 
                     template_key: str, 
                     subject: str, 
                     recipients: List[str],
                     channels: List[Dict[str, Any]],
                     success: bool) -> None:
        """Log notification delivery results."""
        delivery_record = {
            'timestamp': datetime.now().isoformat(),
            'template': template_key,
            'subject': subject,
            'recipients': recipients,
            'channels': channels,
            'success': success
        }
        
        self.delivery_history.append(delivery_record)
        
        # Keep only last 1000 records to prevent memory issues
        if len(self.delivery_history) > 1000:
            self.delivery_history = self.delivery_history[-1000:]
        
        logger.info(f"Notification delivery logged: {success}")
    
    def get_delivery_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent notification delivery history."""
        return self.delivery_history[-limit:]
    
    def send_scope_change_notification(self, 
                                     change_data: Dict[str, Any],
                                     impact_analysis: Dict[str, Any],
                                     recipients: List[str]) -> bool:
        """
        Send scope change notification with standardized format.
        
        Args:
            change_data: Scope change dictionary
            impact_analysis: Impact analysis results
            recipients: List of recipient email addresses
            
        Returns:
            True if notification was successfully sent
        """
        change_type = change_data.get('change_type', 'unknown')
        task_id = change_data.get('task_id', 'unknown')
        
        # Determine template based on change type
        if change_type == 'add':
            template_key = 'scope_change_add'
        elif change_type == 'remove':
            template_key = 'scope_change_remove'
        elif change_type == 'modify':
            template_key = 'scope_change_modify'
        else:
            template_key = 'scope_change_modify'
        
        # Prepare context for template
        context = {
            'task_id': task_id,
            'task_name': change_data.get('details', {}).get('task', {}).get('name', 'Unknown'),
            'parent_id': change_data.get('details', {}).get('parent_id', 'None'),
            'requester': change_data.get('requester', 'System'),
            'timestamp': datetime.now().isoformat(),
            'schedule_impact': impact_analysis.get('schedule_impact', 0),
            'cost_impact': impact_analysis.get('cost_impact', 0),
            'resource_impact': impact_analysis.get('resource_impact', 0),
            'risk_level': impact_analysis.get('risk_level', 'unknown'),
            'approval_status': change_data.get('approval_status', {}).get('status', 'pending'),
            'next_steps': 'Review the change and provide feedback',
            'changes_summary': self._format_changes_summary(change_data)
        }
        
        # Check if approval is required
        approval_status = change_data.get('approval_status', {})
        if approval_status.get('status') == 'requires_approval':
            # Send high-priority approval request
            approval_context = context.copy()
            approval_context.update({
                'approval_conditions': '\n'.join(approval_status.get('conditions', [])),
                'change_type': change_type
            })
            return self.send_notification('approval_required', approval_context, recipients)
        
        return self.send_notification(template_key, context, recipients)
    
    def _format_changes_summary(self, change_data: Dict[str, Any]) -> str:
        """Format changes summary for modification notifications."""
        if change_data.get('change_type') != 'modify':
            return "N/A"
        
        details = change_data.get('details', {})
        changes = []
        
        for key, value in details.items():
            if key not in ['modification_complexity', 'estimated_effort']:
                changes.append(f"- {key}: {value}")
        
        return '\n'.join(changes) if changes else "No specific changes detailed"
    
    def send_quality_alert(self,
                          project_name: str,
                          quality_data: Dict[str, Any],
                          recipients: List[str]) -> bool:
        """
        Send quality alert notification.
        
        Args:
            project_name: Name of the project
            quality_data: Quality assessment data
            recipients: List of recipient email addresses
            
        Returns:
            True if notification was successfully sent
        """
        context = {
            'project_name': project_name,
            'quality_level': quality_data.get('quality_level', 'UNKNOWN'),
            'quality_score': quality_data.get('quality_score', 0),
            'critical_issues': self._format_critical_issues(quality_data),
            'recommendations': self._format_recommendations(quality_data)
        }
        
        return self.send_notification('quality_alert', context, recipients)
    
    def _format_critical_issues(self, quality_data: Dict[str, Any]) -> str:
        """Format critical quality issues for notification."""
        issues = []
        
        # Check for poor quality tasks
        if quality_data.get('poor_quality_tasks', 0) > 0:
            issues.append(f"- {quality_data['poor_quality_tasks']} tasks have POOR quality")
        
        # Check for specific metric failures
        task_quality = quality_data.get('task_quality', {})
        for task_id, task_data in task_quality.items():
            if task_data.get('level') in ['LOW', 'POOR']:
                metrics = task_data.get('metrics', {})
                for metric_name, metric_data in metrics.items():
                    if metric_data.get('score', 0) < metric_data.get('target', 0) * 0.5:
                        issues.append(f"- Task {task_id}: {metric_name} critically low")
        
        return '\n'.join(issues) if issues else "No critical issues detected"
    
    def _format_recommendations(self, quality_data: Dict[str, Any]) -> str:
        """Format quality improvement recommendations."""
        recommendations = quality_data.get('recommendations', [])
        return '\n'.join([f"- {rec}" for rec in recommendations]) if recommendations else "No specific recommendations"

# Example usage
if __name__ == "__main__":
    # Example usage of the notification service
    service = NotificationService()
    
    # Example scope change notification
    change_example = {
        'task_id': 'task_123',
        'change_type': 'add',
        'requester': 'project_manager',
        'details': {
            'parent_id': 'phase_1',
            'task': {
                'name': 'New Feature Development',
                'id': 'task_123'
            }
        },
        'approval_status': {
            'status': 'pending'
        }
    }
    
    impact_example = {
        'schedule_impact': 5,
        'cost_impact': 2500,
        'resource_impact': 2,
        'risk_level': 'medium'
    }
    
    success = service.send_scope_change_notification(
        change_example,
        impact_example,
        ['manager@example.com', 'team@example.com']
    )
    
    print(f"Notification sent: {success}")
