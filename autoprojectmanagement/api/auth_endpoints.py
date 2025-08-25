#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
path: autoprojectmanagement/api/auth_endpoints.py
File: auth_endpoints.py
Purpose: Authentication API endpoints for user management
Author: AutoProjectManagement Team
Version: 1.0.0
License: MIT
Description: REST API endpoints for user authentication, registration, and session management
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from .auth_models import (
    UserRegisterRequest, UserLoginRequest, PasswordResetRequest,
    PasswordResetConfirmRequest, EmailVerifyRequest, TokenRefreshRequest,
    UserUpdateRequest, PasswordChangeRequest, LogoutRequest,
    LoginSuccessResponse, LoginErrorResponse, RegisterSuccessResponse,
    RegisterErrorResponse, AuthTokenResponse, UserProfileResponse,
    TokenRefreshResponse, LogoutResponse, SuccessResponse, ErrorResponse,
    ErrorCodes, SuccessMessages, AuthExamples
)
from ..services.auth_service import auth_service
from ..utils.security import SecurityConfig, token_manager
from ..storage.user_storage import user_storage_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# HTTP Bearer scheme for token authentication
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP bearer credentials
        
    Returns:
        User information from token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = auth_service.validate_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return payload

@router.post(
    "/register",
    response_model=RegisterSuccessResponse,
    responses={
        400: {"model": RegisterErrorResponse},
        409: {"model": RegisterErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Register new user",
    description="Create a new user account with email verification"
)
async def register_user(
    request: Request,
    user_data: UserRegisterRequest
):
    """
    Register a new user account.
    
    Creates a new user with email verification requirement.
    Password must meet complexity requirements.
    
    Args:
        user_data: User registration data
        
    Returns:
        Registration success response with user ID
        
    Raises:
        HTTPException: If registration fails
    """
    try:
        success, message, user_profile = auth_service.register_user(user_data)
        
        if success:
            return RegisterSuccessResponse(
                success=True,
                message=message,
                user_id=user_profile.user_id,
                email=user_profile.email
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post(
    "/login",
    response_model=LoginSuccessResponse,
    responses={
        400: {"model": LoginErrorResponse},
        401: {"model": LoginErrorResponse},
        429: {"model": LoginErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="User login",
    description="Authenticate user and create session"
)
async def login_user(
    request: Request,
    login_data: UserLoginRequest
):
    """
    Authenticate user and create session.
    
    Validates user credentials and returns JWT tokens.
    Includes rate limiting to prevent brute force attacks.
    
    Args:
        login_data: User login credentials
        
    Returns:
        Authentication tokens and user information
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Get user agent and IP address for session tracking
        user_agent = request.headers.get("User-Agent")
        ip_address = request.client.host if request.client else None
        
        success, message, auth_data = auth_service.login_user(
            login_data, user_agent, ip_address
        )
        
        if success:
            return LoginSuccessResponse(
                success=True,
                message=message,
                data=auth_data
            )
        else:
            # Determine appropriate status code
            status_code = status.HTTP_401_UNAUTHORIZED
            error_code = ErrorCodes.INVALID_CREDENTIALS
            
            if "verify" in message.lower():
                status_code = status.HTTP_403_FORBIDDEN
                error_code = ErrorCodes.ACCOUNT_NOT_VERIFIED
            elif "attempts" in message.lower():
                status_code = status.HTTP_429_TOO_MANY_REQUESTS
                error_code = ErrorCodes.RATE_LIMITED
            
            raise HTTPException(
                status_code=status_code,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post(
    "/logout",
    response_model=LogoutResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="User logout",
    description="Invalidate user session"
)
