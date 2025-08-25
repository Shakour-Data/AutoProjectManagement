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
