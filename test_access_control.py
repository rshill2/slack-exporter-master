#!/usr/bin/env python3
"""
Test script to verify access control functionality.
Run this to check if user and channel restrictions are working correctly.
"""

import os
import sys
from config import (
    add_allowed_user, remove_allowed_user, add_allowed_channel, remove_allowed_channel,
    is_user_allowed, is_channel_allowed, list_allowed_users, list_allowed_channels,
    clear_allowed_users, clear_allowed_channels
)

def test_user_management():
    """Test user management functions"""
    print("🧪 Testing User Management")
    print("-" * 30)
    
    # Clear existing users
    clear_allowed_users()
    assert len(list_allowed_users()) == 0, "Failed to clear users"
    print("✅ Cleared existing users")
    
    # Test adding valid user
    assert add_allowed_user("U097LRDRB8F"), "Failed to add valid user"
    assert is_user_allowed("U097LRDRB8F"), "User not found after adding"
    print("✅ Added valid user: U097LRDRB8F")
    
    # Test adding invalid user
    assert not add_allowed_user("invalid_user"), "Should reject invalid user ID"
    print("✅ Rejected invalid user ID")
    
    # Test removing user
    assert remove_allowed_user("U097LRDRB8F"), "Failed to remove user"
    assert not is_user_allowed("U097LRDRB8F"), "User still allowed after removal"
    print("✅ Removed user successfully")
    
    # Test removing non-existent user
    assert not remove_allowed_user("U9999999999"), "Should fail to remove non-existent user"
    print("✅ Correctly handled non-existent user removal")

def test_channel_management():
    """Test channel management functions"""
    print("\n🧪 Testing Channel Management")
    print("-" * 30)
    
    # Clear existing channels
    clear_allowed_channels()
    assert len(list_allowed_channels()) == 0, "Failed to clear channels"
    print("✅ Cleared existing channels")
    
    # Test adding valid channel
    assert add_allowed_channel("C099EEMH26N"), "Failed to add valid channel"
    assert is_channel_allowed("C099EEMH26N"), "Channel not found after adding"
    print("✅ Added valid channel: C099EEMH26N")
    
    # Test adding invalid channel
    assert not add_allowed_channel("invalid_channel"), "Should reject invalid channel ID"
    print("✅ Rejected invalid channel ID")
    
    # Test removing channel
    assert remove_allowed_channel("C099EEMH26N"), "Failed to remove channel"
    assert not is_channel_allowed("C099EEMH26N"), "Channel still allowed after removal"
    print("✅ Removed channel successfully")
    
    # Test removing non-existent channel
    assert not remove_allowed_channel("C9999999999"), "Should fail to remove non-existent channel"
    print("✅ Correctly handled non-existent channel removal")

def test_access_control():
    """Test access control logic"""
    print("\n🧪 Testing Access Control Logic")
    print("-" * 30)
    
    # Set up test data
    clear_allowed_users()
    clear_allowed_channels()
    
    add_allowed_user("U097LRDRB8F")
    add_allowed_channel("C099EEMH26N")
    
    # Test allowed user and channel
    assert is_user_allowed("U097LRDRB8F"), "Allowed user should be permitted"
    assert is_channel_allowed("C099EEMH26N"), "Allowed channel should be permitted"
    print("✅ Access granted for allowed user and channel")
    
    # Test denied user and channel
    assert not is_user_allowed("U9999999999"), "Denied user should be blocked"
    assert not is_channel_allowed("C9999999999"), "Denied channel should be blocked"
    print("✅ Access denied for unauthorized user and channel")
    
    # Test with empty lists (should allow all)
    clear_allowed_users()
    clear_allowed_channels()
    
    # Note: The current implementation requires explicit allowlisting
    # This test verifies the current behavior
    assert not is_user_allowed("U097LRDRB8F"), "User should be denied when not in allowlist"
    assert not is_channel_allowed("C099EEMH26N"), "Channel should be denied when not in allowlist"
    print("✅ Access control works with empty allowlists")

def test_persistence():
    """Test that data persists between function calls"""
    print("\n🧪 Testing Data Persistence")
    print("-" * 30)
    
    # Clear and add test data
    clear_allowed_users()
    clear_allowed_channels()
    
    add_allowed_user("U097LRDRB8F")
    add_allowed_channel("C099EEMH26N")
    
    # Verify data is persisted
    users = list_allowed_users()
    channels = list_allowed_channels()
    
    assert "U097LRDRB8F" in users, "User not persisted"
    assert "C099EEMH26N" in channels, "Channel not persisted"
    assert len(users) == 1, "Wrong number of users"
    assert len(channels) == 1, "Wrong number of channels"
    
    print("✅ Data persistence working correctly")

def main():
    """Run all tests"""
    print("🔧 Testing Slack Exporter Access Control")
    print("=" * 50)
    
    try:
        test_user_management()
        test_channel_management()
        test_access_control()
        test_persistence()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Access control is working correctly.")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
