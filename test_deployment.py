#!/usr/bin/env python3
"""
Test script to verify deployment readiness.
This script tests that all imports work and the Flask app can start.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✅ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    try:
        import pathvalidate
        print("✅ Pathvalidate imported successfully")
    except ImportError as e:
        print(f"❌ Pathvalidate import failed: {e}")
        return False
    
    try:
        import gunicorn
        print("✅ Gunicorn imported successfully")
    except ImportError as e:
        print(f"❌ Gunicorn import failed: {e}")
        return False
    
    return True

def test_bot_imports():
    """Test that bot.py can be imported"""
    print("\n🧪 Testing bot.py imports...")
    
    try:
        # Test importing the main modules
        from exporter import post_response, channel_history
        print("✅ Exporter module imported successfully")
    except ImportError as e:
        print(f"⚠️  Exporter module import failed: {e}")
        print("   This is expected if SLACK_USER_TOKEN is not set")
    
    try:
        from config import is_user_allowed, is_channel_allowed
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"⚠️  Config module import failed: {e}")
        print("   This is expected if config files don't exist yet")
    
    return True

def test_flask_app():
    """Test that the Flask app can be created"""
    print("\n🧪 Testing Flask app creation...")
    
    try:
        # Import the app from bot.py
        from bot import app
        print("✅ Flask app imported successfully")
        
        # Test that it's a Flask app
        if hasattr(app, 'route'):
            print("✅ Flask app has route decorator")
        else:
            print("❌ Flask app missing route decorator")
            return False
        
        # Test that health endpoint exists
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint returned {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("\n🧪 Testing environment...")
    
    # Check if we're in a deployment environment
    port = os.environ.get('PORT')
    if port:
        print(f"✅ PORT environment variable set: {port}")
    else:
        print("⚠️  PORT environment variable not set (this is normal for local development)")
    
    # Check for Slack token
    slack_token = os.environ.get('SLACK_USER_TOKEN')
    if slack_token:
        print("✅ SLACK_USER_TOKEN environment variable set")
    else:
        print("⚠️  SLACK_USER_TOKEN environment variable not set")
        print("   This is required for full functionality")
    
    return True

def main():
    """Run all deployment tests"""
    print("🔧 Testing Deployment Readiness")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test basic imports
    if not test_imports():
        all_tests_passed = False
    
    # Test bot imports
    if not test_bot_imports():
        all_tests_passed = False
    
    # Test Flask app
    if not test_flask_app():
        all_tests_passed = False
    
    # Test environment
    if not test_environment():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✅ All tests passed! Application is ready for deployment.")
        print("\n📋 Deployment Checklist:")
        print("   - Set SLACK_USER_TOKEN environment variable")
        print("   - Configure allowed users and channels")
        print("   - Test Slack integration")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
