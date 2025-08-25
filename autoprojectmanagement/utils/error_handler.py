#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/utils/error_handler.py
File: error_handler.py
Purpose: Comprehensive error handling system for AutoProjectManagement
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: Centralized error handling with logging, validation, and user-friendly messages
"""

import logging
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List, Union, Type, Callable
from enum import Enum
import inspect
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for classification."""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATABASE = "database"
    NETWORK = "network"
    FILE_SYSTEM = "file_system"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    UNKNOWN = "unknown"

class ErrorContext:
    """Context information for error reporting."""
    
    def __init__(self, 
                 request_id: Optional[str] = None,
                 user_id: Optional[str] = None,
                 endpoint: Optional[str] = None,
                 method: Optional[str] = None,
                 parameters: Optional[Dict[str, Any]] = None):
        self.request_id = request_id
        self.user_id = user_id
        self.endpoint = endpoint
        self.method = method
        self.parameters = parameters or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "endpoint": self.endpoint,
            "method": self.method,
            "parameters": self.parameters
        }

class CustomError(Exception):
    """Base custom error class with enhanced functionality."""
    
    def __init__(self, 
                 message: str,
                 code: str,
                 severity: ErrorSeverity = ErrorSeverity.ERROR,
                 category: ErrorCategory = ErrorCategory.UNKNOWN,
                 details: Optional[Dict[str, Any]] = None,
                 context: Optional[ErrorContext] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.severity = severity
        self.category = category
        self.details = details or {}
        self.context = context
        self.timestamp = datetime.now()
        self.stack_trace = traceback.format_exc()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for serialization."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "severity": self.severity.value,
                "category": self.category.value,
                "timestamp": self.timestamp.isoformat(),
                "details": self.details,
                "context": self.context.to_dict() if self.context else None
            }
        }
    
    def log(self) -> None:
        """Log the error with appropriate severity."""
        log_message = f"{self.code}: {self.message}"
        if self.context:
            log_message += f" | Context: {json.dumps(self.context.to_dict())}"
        
        if self.severity == ErrorSeverity.DEBUG:
            logger.debug(log_message, exc_info=True)
        elif self.severity == ErrorSeverity.INFO:
            logger.info(log_message)
        elif self.severity == ErrorSeverity.WARNING:
            logger.warning(log_message, exc_info=True)
        elif self.severity == ErrorSeverity.ERROR:
            logger.error(log_message, exc_info=True)
        elif self.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message, exc_info=True)

class ValidationError(CustomError):
    """Error for validation failures."""
    
    def __init__(self, 
                 message: str,
                 field: Optional[str] = None,
                 value: Optional[Any] = None,
                 context: Optional[ErrorContext] = None):
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
