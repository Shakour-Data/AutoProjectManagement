# Authentication Models Documentation

## Overview
This document provides detailed information about the Pydantic models used in the authentication system of AutoProjectManagement. These models define the structure of request and response data for authentication endpoints.

## Request Models

### 1. UserRegisterRequest
Used for user registration requests.

**Fields:**
- `email` (EmailStr): User's email address (must be valid email format)
- `password` (str): User's password (min 8 characters, must contain uppercase, lowercase, and digits)
- `first_name` (str): User's first name (1-50 characters)
- `last_name` (str): User's last name (1-50 characters)

**Example:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
}
```

### 2. UserLoginRequest
Used for user login requests.

**Fields:**
- `email` (EmailStr): User's email address
- `password` (str): User's password

**Example:**
```json
{
    "email": "user@example.com",
    "password": "SecurePass123!"
}
```

### 3. PasswordResetRequest
Used for requesting password reset.

**Fields:**
- `email` (EmailStr): User's email address

**Example:**
```json
{
    "email": "user@example.com"
}
```

### 4. PasswordResetConfirmRequest
Used for confirming password reset.

**Fields:**
- `token` (str): Password reset token
- `new_password` (str): New password (must meet complexity requirements)

**Example:**
```json
{
    "token": "abc123def456",
    "new_password": "NewSecurePass123!"
}
```

## Response Models

### 1. UserProfileResponse
Contains user profile information.

**Fields:**
- `user_id` (str): Unique user identifier
- `email` (EmailStr): User's email address
- `first_name` (str): User's first name
- `last_name` (str): User's last name
- `is_verified` (bool): Whether email is verified
- `is_active` (bool): Whether account is active
- `created_at` (datetime): Account creation timestamp
- `last_login` (datetime): Last login timestamp (optional)

### 2. AuthTokenResponse
Contains authentication tokens.

**Fields:**
- `access_token` (str): JWT access token
- `refresh_token` (str): JWT refresh token
- `token_type` (str): Token type (always "bearer")
- `expires_in` (int): Token expiration time in seconds
- `user` (UserProfileResponse): User profile information

### 3. SuccessResponse
Generic success response.

**Fields:**
- `success` (bool): Operation success status (always true)
- `message` (str): Success message
- `data` (dict): Response data (optional)

### 4. ErrorResponse
Generic error response.

**Fields:**
- `success` (bool): Operation success status (always false)
- `error` (str): Error message
- `detail` (str): Error details (optional)
- `error_code` (str): Error code for client handling (optional)

## Error Codes

The authentication system uses standardized error codes:

- `auth_user_exists`: User already exists
- `auth_invalid_credentials`: Invalid login credentials
- `auth_account_not_verified`: Account email not verified
- `auth_account_locked`: Account locked due to too many failed attempts
- `auth_invalid_token`: Invalid authentication token
- `auth_expired_token`: Expired authentication token
- `auth_password_weak`: Password doesn't meet complexity requirements
- `auth_rate_limited`: Too many requests
- `auth_user_not_found`: User not found

## Usage Examples

### Registration Example
```python
from autoprojectmanagement.api.auth_models import UserRegisterRequest

register_data = UserRegisterRequest(
    email="user@example.com",
    password="SecurePass123!",
    first_name="John",
    last_name="Doe"
)
```

### Login Example
```python
from autoprojectmanagement.api.auth_models import UserLoginRequest

login_data = UserLoginRequest(
    email="user@example.com",
    password="SecurePass123!"
)
```

## Conclusion
These models provide a structured way to handle authentication data throughout the system. They include validation rules and ensure data consistency across all authentication operations.
