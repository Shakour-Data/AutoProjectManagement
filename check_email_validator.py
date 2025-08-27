#!/usr/bin/env python3
"""
Check if email-validator is working correctly
"""

try:
    import email_validator
    print("✅ email-validator is available")
    print(f"Version: {email_validator.__version__}")
    
    # Test basic email validation
    from email_validator import validate_email, EmailNotValidError
    
    try:
        email = "test@example.com"
        valid = validate_email(email)
        print(f"✅ Email validation works: {valid.email}")
    except EmailNotValidError as e:
        print(f"❌ Email validation error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
except ImportError as e:
    print(f"❌ email-validator not available: {e}")
    print("Try installing with: pip install email-validator")
