#!/usr/bin/env python3
"""
Test script to verify Slack configuration and basic functionality.
Run this to check if your Slack token and permissions are working correctly.
"""

import os
import sys
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def test_slack_connection():
    """Test basic Slack API connection"""
    try:
        token = os.environ.get("SLACK_USER_TOKEN")
        if not token:
            print("❌ SLACK_USER_TOKEN not found in environment variables")
            print("   Please set it in your .env file or environment")
            return False
        
        if not token.startswith("xoxp-"):
            print("❌ Invalid token format. Token should start with 'xoxp-'")
            return False
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test auth.test endpoint
        response = requests.get("https://slack.com/api/auth.test", headers=headers)
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ Slack API error: {data.get('error', 'Unknown error')}")
            return False
        
        print(f"✅ Connected to Slack workspace: {data.get('team', 'Unknown')}")
        print(f"   User: {data.get('user', 'Unknown')}")
        print(f"   Team: {data.get('team', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_permissions():
    """Test if the app has the required permissions"""
    try:
        token = os.environ.get("SLACK_USER_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test conversations.list (requires channels:read)
        response = requests.get("https://slack.com/api/conversations.list", 
                              headers=headers, 
                              params={"limit": 1})
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ Permission test failed: {data.get('error', 'Unknown error')}")
            return False
        
        print("✅ Basic permissions working")
        return True
        
    except Exception as e:
        print(f"❌ Permission test failed: {e}")
        return False

def test_file_access():
    """Test file access permissions"""
    try:
        token = os.environ.get("SLACK_USER_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test files.list (requires files:read)
        response = requests.get("https://slack.com/api/files.list", 
                              headers=headers, 
                              params={"limit": 1})
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ File access test failed: {data.get('error', 'Unknown error')}")
            return False
        
        print("✅ File access permissions working")
        return True
        
    except Exception as e:
        print(f"❌ File access test failed: {e}")
        return False

def main():
    print("🔧 Testing Slack Exporter Configuration")
    print("=" * 40)
    
    # Test connection
    if not test_slack_connection():
        sys.exit(1)
    
    # Test permissions
    if not test_permissions():
        print("⚠️  Some permissions may be missing")
    
    # Test file access
    if not test_file_access():
        print("⚠️  File access permissions may be missing")
    
    print("\n✅ Configuration test completed!")
    print("   Your Slack exporter should be ready to use.")

if __name__ == "__main__":
    main()
