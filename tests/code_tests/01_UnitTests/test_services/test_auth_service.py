import unittest
from src.autoprojectmanagement.services.auth_service import AuthService
from src.autoprojectmanagement.models.user import UserCreate, UserLogin

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()

    def test_register_user_success(self):
        user_data = UserCreate(email="test@example.com", password="StrongPassword123", first_name="Test", last_name="User")
        success, message, user_profile = self.auth_service.register_user(user_data)
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully. Please verify your email.")

    def test_register_user_existing_email(self):
        user_data = UserCreate(email="test@example.com", password="StrongPassword123", first_name="Test", last_name="User")
        self.auth_service.register_user(user_data)  # Register first time
        success, message, _ = self.auth_service.register_user(user_data)  # Try to register again
        self.assertFalse(success)
        self.assertEqual(message, "User with this email already exists")

    def test_login_user_success(self):
        user_data = UserCreate(email="test@example.com", password="StrongPassword123", first_name="Test", last_name="User")
        self.auth_service.register_user(user_data)  # Register user first
        login_data = UserLogin(email="test@example.com", password="StrongPassword123")
        success, message, auth_data = self.auth_service.login_user(login_data)
        self.assertTrue(success)
        self.assertEqual(message, "Login successful")

    def test_login_user_invalid_credentials(self):
        login_data = UserLogin(email="test@example.com", password="WrongPassword")
        success, message, _ = self.auth_service.login_user(login_data)
        self.assertFalse(success)
        self.assertEqual(message, "Invalid credentials")

    def test_request_password_reset(self):
        user_data = UserCreate(email="test@example.com", password="StrongPassword123", first_name="Test", last_name="User")
        self.auth_service.register_user(user_data)  # Register user first
        reset_request = PasswordResetRequest(email="test@example.com")
        success, message = self.auth_service.request_password_reset(reset_request)
        self.assertTrue(success)
        self.assertEqual(message, "If the email exists, a reset link has been sent")

if __name__ == "__main__":
    unittest.main()
