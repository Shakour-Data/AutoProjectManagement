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
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.VALIDATION,
            details=details,
            context=context
        )

class AuthenticationError(CustomError):
    """Error for authentication failures."""
    
    def __init__(self, 
                 message: str,
                 context: Optional[ErrorContext] = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.AUTHENTICATION,
            context=context
        )

class AuthorizationError(CustomError):
    """Error for authorization failures."""
    
    def __init__(self, 
                 message: str,
                 context: Optional[ErrorContext] = None):
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.AUTHORIZATION,
            context=context
        )

class DatabaseError(CustomError):
    """Error for database operations."""
    
    def __init__(self, 
                 message: str,
                 operation: Optional[str] = None,
                 context: Optional[ErrorContext] = None):
        details = {"operation": operation} if operation else {}
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.DATABASE,
            details=details,
            context=context
        )

class ErrorHandler:
    """Centralized error handling system."""
    
    def __init__(self, log_errors: bool = True, raise_errors: bool = False):
        self.log_errors = log_errors
        self.raise_errors = raise_errors
        self.error_log: List[Dict[str, Any]] = []
    
    def handle_error(self, 
                    error: Exception,
                    context: Optional[ErrorContext] = None) -> Dict[str, Any]:
        """
        Handle an error with comprehensive logging and reporting.
        
        Args:
            error: The exception to handle
            context: Additional context information
            
        Returns:
            Dictionary with error information
        """
        # Convert standard exceptions to custom errors
        if not isinstance(error, CustomError):
            error = self._convert_standard_error(error, context)
        
        # Log the error
        if self.log_errors:
            error.log()
            self.error_log.append({
                "timestamp": datetime.now().isoformat(),
                "error": error.to_dict(),
                "context": context.to_dict() if context else None
            })
        
        # Raise if configured to do so
        if self.raise_errors:
            raise error
        
        return error.to_dict()
    
    def _convert_standard_error(self, 
                               error: Exception,
                               context: Optional[ErrorContext]) -> CustomError:
        """Convert standard Python exceptions to custom errors."""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Map common exception types to custom errors
        if "validation" in error_message.lower() or "invalid" in error_message.lower():
            return ValidationError(
                message=error_message,
                context=context
            )
        elif "permission" in error_message.lower() or "access denied" in error_message.lower():
            return AuthorizationError(
                message=error_message,
                context=context
            )
        elif "authentication" in error_message.lower() or "login" in error_message.lower():
            return AuthenticationError(
                message=error_message,
                context=context
            )
        elif "database" in error_message.lower() or "sql" in error_message.lower():
            return DatabaseError(
                message=error_message,
                context=context
            )
        else:
            return CustomError(
                message=error_message,
                code=f"GENERIC_{error_type.upper()}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.UNKNOWN,
                context=context
            )
    
    def validate_input(self, 
                      data: Any,
                      validation_rules: Dict[str, Any],
