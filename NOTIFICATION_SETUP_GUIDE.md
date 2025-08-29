# Notification Service Setup Guide

## Overview

This guide explains how to configure and use the AutoProjectManagement Notification Service for scope change alerts and quality notifications.

## Configuration File

The notification service uses `data/inputs/UserInputs/notification_config.json` for configuration. This file contains settings for:

- Email (SMTP) configuration
- Slack webhook integration  
- Microsoft Teams webhook integration
- Default recipients
- Notification preferences

## Email Configuration

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account Settings → Security
   - Under "Signing in to Google", enable 2-Step Verification
   - Click "App passwords" and generate a new app password
   - Select "Mail" and "Other (Custom name)" - name it "AutoProjectManagement"

3. **Update notification_config.json**:
```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your.email@gmail.com",
    "password": "your-app-password-here",
    "from_address": "your.email@gmail.com",
    "use_tls": true
  }
}
```

### Outlook/Office 365 Setup

```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.office365.com",
    "smtp_port": 587,
    "username": "your.email@company.com",
    "password": "your-password",
    "from_address": "your.email@company.com",
    "use_tls": true
  }
}
```

### Other SMTP Providers

For other providers (SendGrid, Mailgun, etc.), use their specific SMTP settings.

## Testing the Configuration

Run the test script to verify your setup:

```bash
python test_notification_service.py
```

This will:
1. Check your configuration
2. Send a test scope change notification
3. Show delivery status

## Notification Templates

The service uses templates located in `data/inputs/UserInputs/notification_templates.json`. Available templates:

- `scope_change_add` - New task added to scope
- `scope_change_remove` - Task removed from scope  
- `scope_change_modify` - Task modified
- `approval_required` - High-priority approval requests
- `quality_alert` - Quality issues detected

## Default Recipients

Configure default recipients in the config file:

```json
{
  "default_recipients": [
    "project.manager@company.com",
    "team.lead@company.com"
  ],
  "high_priority_recipients": [
    "senior.management@company.com"
  ]
}
```

## Notification Preferences

Control which notifications are sent:

```json
{
  "notification_preferences": {
    "scope_change_add": true,
    "scope_change_remove": true,
    "scope_change_modify": true,
    "approval_required": true,
    "quality_alert": true,
    "baseline_created": true,
    "baseline_restored": true
  }
}
```

## Integration with Scope Management

The notification service integrates automatically with the scope management module. When scope changes occur, notifications are sent to:

1. Project managers
2. Team leads  
3. Quality assurance
4. Senior management (for high-risk changes)

## Troubleshooting

### Common Issues

1. **Authentication failed**
   - Check username/password
   - For Gmail: Use app password, not regular password
   - Enable less secure apps if required by provider

2. **Connection refused**
   - Check SMTP server and port
   - Verify firewall settings
   - Check if TLS is required

3. **No notifications sent**
   - Check if email is enabled in config
   - Verify recipient addresses
   - Check notification preferences

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- Store sensitive credentials in environment variables or secure config files
- Use app-specific passwords instead of main account passwords
- Regularly rotate passwords and access tokens
- Restrict access to configuration files

## Support

For additional help, check:
- SMTP provider documentation
- Project documentation in `/docs/`
- Test scripts in the repository
