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
async def logout_user(
    request: Request,
    logout_data: Optional[LogoutRequest] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Log out user and invalidate session.
    
    Can invalidate specific session or all sessions for the user.
    
    Args:
        logout_data: Optional session ID to invalidate
        current_user: Authenticated user from token
        
    Returns:
        Logout success response
        
    Raises:
        HTTPException: If logout fails
    """
    try:
        # For simplicity, we'll invalidate all sessions for the user
        # In production, you might want more granular session management
        user_id = current_user.get("sub")
        
        # Find and remove all sessions for this user
        sessions_to_remove = [
            session_id for session_id, session in user_storage_service.user_storage.sessions.items()
            if session.user_id == user_id
        ]
        
        for session_id in sessions_to_remove:
            auth_service.logout_user(session_id)
        
        return LogoutResponse(
            success=True,
            message=SuccessMessages.LOGOUT_SUCCESS
        )
            
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )

@router.post(
    "/verify-email",
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Verify email address",
    description="Verify user email using verification token"
)
async def verify_email(
    request: Request,
    verify_data: EmailVerifyRequest
):
    """
    Verify user email address.
    
    Uses verification token sent to user's email.
    
    Args:
        verify_data: Email verification data
        
    Returns:
        Verification success response
        
    Raises:
        HTTPException: If verification fails
    """
    try:
        success, message = auth_service.verify_email(verify_data.token)
        
        if success:
            return SuccessResponse(
                success=True,
                message=message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email verification failed: {str(e)}"
        )

@router.post(
    "/request-password-reset",
    response_model=SuccessResponse,
    responses={
        500: {"model": ErrorResponse}
    },
    summary="Request password reset",
    description="Send password reset email to user"
)
async def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest
):
    """
    Request password reset for user.
    
    Sends password reset email with token (in real implementation).
    
    Args:
        reset_request: Password reset request data
        
    Returns:
        Success response (always returns success for security)
        
    Raises:
        HTTPException: If request fails
    """
    try:
        success, message = auth_service.request_password_reset(reset_request)
        
        return SuccessResponse(
            success=True,
            message=message
        )
            
    except Exception as e:
        logger.error(f"Password reset request error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset request failed: {str(e)}"
        )

@router.post(
    "/reset-password",
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Reset password",
    description="Reset user password using reset token"
)
async def reset_password(
    request: Request,
    reset_confirm: PasswordResetConfirmRequest
):
    """
    Reset user password using reset token.
    
    Validates reset token and updates user password.
    
    Args:
        reset_confirm: Password reset confirmation data
        
    Returns:
        Password reset success response
        
    Raises:
        HTTPException: If password reset fails
    """
    try:
        success, message = auth_service.reset_password(reset_confirm)
        
        if success:
            return SuccessResponse(
                success=True,
                message=message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )

@router.post(
    "/refresh-token",
    response_model=TokenRefreshResponse,
    responses={
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Refresh access token",
    description="Refresh JWT access token using refresh token"
)
async def refresh_token(
    request: Request,
    refresh_request: TokenRefreshRequest
):
    """
    Refresh JWT access token.
    
    Uses refresh token to generate new access token.
    
    Args:
        refresh_request: Token refresh request data
        
    Returns:
        New access token response
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        success, message, auth_data = auth_service.refresh_access_token(
            refresh_request.refresh_token
        )
        
        if success:
            return TokenRefreshResponse(
                access_token=auth_data["access_token"],
                token_type=auth_data["token_type"],
                expires_in=auth_data["expires_in"]
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )

@router.get(
    "/profile",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get user profile",
    description="Get current authenticated user's profile information"
)
async def get_profile(
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get user profile information.
    
    Returns profile data for authenticated user.
    
    Args:
        current_user: Authenticated user from token
        
    Returns:
        User profile response
        
    Raises:
        HTTPException: If profile retrieval fails
    """
    try:
        user_id = current_user.get("sub")
        user_profile = auth_service.get_user_by_id(user_id)
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        return user_profile
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile retrieval error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile retrieval failed: {str(e)}"
        )

@router.put(
    "/profile",
    response_model=SuccessResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Update user profile",
    description="Update current user's profile information"
)
async def update_profile(
    request: Request,
    update_data: UserUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update user profile information.
    
    Allows updating name and email (with re-verification).
    
    Args:
        update_data: Profile update data
        current_user: Authenticated user from token
        
    Returns:
        Update success response
        
    Raises:
        HTTPException: If profile update fails
    """
    try:
        # This is a placeholder implementation
        # In real implementation, you would update the user profile
        # and handle email verification if email is changed
        
        user_id = current_user.get("sub")
        user_profile = auth_service.get_user_by_id(user_id)
        
        if not user_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        # Update profile fields (simplified implementation)
        if update_data.first_name:
            user_profile.first_name = update_data.first_name
        
        if update_data.last_name:
            user_profile.last_name = update_data.last_name
        
        # Email change would require verification
        if update_data.email and update_data.email != user_profile.email:
            # In real implementation, you would:
            # 1. Send verification email to new address
            # 2. Keep old email until verification is complete
            # 3. Update email after verification
            user_profile.email = update_data.email
            user_profile.is_verified = False  # Require re-verification
        
        user_storage_service.save_data()
        
        return SuccessResponse(
            success=True,
            message=SuccessMessages.PROFILE_UPDATED
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile update failed: {str(e)}"
        )

@router.get(
    "/config",
    response_model=Dict[str, Any],
    summary="Get auth configuration",
    description="Get authentication system configuration"
)
async def get_auth_config(request: Request):
    """
    Get authentication configuration.
    
    Returns password requirements, session settings, etc.
    
    Returns:
        Authentication configuration
    """
    return {
        "password_min_length": SecurityConfig.PASSWORD_MIN_LENGTH,
        "password_requirements": {
            "min_length": SecurityConfig.PASSWORD_MIN_LENGTH,
            "max_length": SecurityConfig.PASSWORD_MAX_LENGTH,
            "requires_uppercase": True,
            "requires_lowercase": True,
            "requires_digit": True,
            "requires_special": False
        },
        "session_timeout_minutes": SecurityConfig.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_expire_days": SecurityConfig.JWT_REFRESH_TOKEN_EXPIRE_DAYS,
        "max_login_attempts": SecurityConfig.MAX_LOGIN_ATTEMPTS,
        "lockout_minutes": SecurityConfig.LOGIN_LOCKOUT_MINUTES
    }

# Error handlers
@router.get("/health", include_in_schema=False)
async def auth_health_check():
    """Health check endpoint for authentication service."""
    return {"status": "healthy", "service": "authentication"}

# Include this in your main app to handle validation errors
async def validation_exception_handler(request, exc):
    """Handle validation errors with consistent format."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation failed",
            "detail": exc.errors()
        }
    )
