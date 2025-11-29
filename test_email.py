#!/usr/bin/env python3
"""
Test email functionality
"""

from coach_saas_app import send_email

def test_email_system():
    """Test the email notification system"""
    print("=== Testing Email System ===")
    
    # Test email sending
    result = send_email(
        to_email="test@example.com",
        subject="Test Email - Coach Institute SaaS",
        body="""
        <h2>Test Email</h2>
        <p>This is a test email from the Coach Institute SaaS platform.</p>
        <p>If you see this in console output, the email system is working correctly.</p>
        """
    )
    
    if result:
        print("[SUCCESS] Email system is working!")
        print("\nTo enable real email sending:")
        print("1. Set environment variables:")
        print("   SENDER_EMAIL=your-gmail@gmail.com")
        print("   SENDER_PASSWORD=your-gmail-app-password")
        print("2. Restart the application")
    else:
        print("[ERROR] Email system failed")
    
    return result

if __name__ == '__main__':
    test_email_system()