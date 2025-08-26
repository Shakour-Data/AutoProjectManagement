# Authentication API Documentation

## Overview
This document provides an overview of the authentication API endpoints available in the AutoProjectManagement system. The authentication system supports user registration, login, password management, and profile management.

## Endpoints

### 1. User Registration
- **Endpoint**: `/auth/register`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "first_name": "John",
        "last_name": "Doe"
    }
    ```
- **Responses**:
    - **201 Created**: User registered successfully.
    - **400 Bad Request**: Validation errors.
    - **409 Conflict**: User already exists.

### 2. User Login
- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    ```
- **Responses**:
    - **200 OK**: Login successful, returns access and refresh tokens.
    - **401 Unauthorized**: Invalid credentials.
    - **403 Forbidden**: Account not verified.

### 3. Password Reset Request
- **Endpoint**: `/auth/request-password-reset`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "email": "user@example.com"
    }
    ```
- **Responses**:
    - **200 OK**: Password reset email sent.
    - **404 Not Found**: User not found.

### 4. Password Reset Confirmation
- **Endpoint**: `/auth/reset-password`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "token": "reset_token",
        "new_password": "NewSecurePass123!"
    }
    ```
- **Responses**:
    - **200 OK**: Password reset successfully.
    - **400 Bad Request**: Invalid token or weak password.

### 5. User Profile
- **Endpoint**: `/auth/profile`
- **Method**: `GET`
- **Responses**:
    - **200 OK**: Returns user profile information.
    - **401 Unauthorized**: Invalid or expired token.

### 6. User Logout
- **Endpoint**: `/auth/logout`
- **Method**: `POST`
- **Responses**:
    - **200 OK**: Logout successful.
    - **401 Unauthorized**: Invalid token.

## Error Handling
All endpoints return appropriate HTTP status codes and error messages for various scenarios, including validation errors, unauthorized access, and server errors.

## Testing
To test the authentication API, use tools like Postman or curl to send requests to the endpoints and verify the responses.

## Conclusion
This document serves as a guide for developers to understand and utilize the authentication API effectively. Ensure to follow the API specifications for successful integration.
