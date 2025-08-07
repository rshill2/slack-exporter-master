#!/usr/bin/env python3
"""
Management script for Slack Exporter access control.
Use this script to manage which users and channels are allowed to use the exporter.
"""

import argparse
import sys
from config import (
    add_allowed_user, remove_allowed_user, add_allowed_channel, remove_allowed_channel,
    list_allowed_users, list_allowed_channels, clear_allowed_users, clear_allowed_channels
)

def print_users():
    """Print all allowed users"""
    users = list_allowed_users()
    if users:
        print("✅ Allowed Users:")
        for user in users:
            print(f"  - {user}")
        print(f"Total: {len(users)} users")
    else:
        print("❌ No users are currently allowed")

def print_channels():
    """Print all allowed channels"""
    channels = list_allowed_channels()
    if channels:
        print("✅ Allowed Channels:")
        for channel in channels:
            print(f"  - {channel}")
        print(f"Total: {len(channels)} channels")
    else:
        print("❌ No channels are currently allowed")

def add_user(user_id):
    """Add a user to the allowed list"""
    if add_allowed_user(user_id):
        print(f"✅ User {user_id} added successfully")
        print_users()
    else:
        print(f"❌ Failed to add user {user_id}")
        sys.exit(1)

def remove_user(user_id):
    """Remove a user from the allowed list"""
    if remove_allowed_user(user_id):
        print(f"✅ User {user_id} removed successfully")
        print_users()
    else:
        print(f"❌ Failed to remove user {user_id}")
        sys.exit(1)

def add_channel(channel_id):
    """Add a channel to the allowed list"""
    if add_allowed_channel(channel_id):
        print(f"✅ Channel {channel_id} added successfully")
        print_channels()
    else:
        print(f"❌ Failed to add channel {channel_id}")
        sys.exit(1)

def remove_channel(channel_id):
    """Remove a channel from the allowed list"""
    if remove_allowed_channel(channel_id):
        print(f"✅ Channel {channel_id} removed successfully")
        print_channels()
    else:
        print(f"❌ Failed to remove channel {channel_id}")
        sys.exit(1)

def clear_users():
    """Clear all allowed users"""
    if clear_allowed_users():
        print("✅ All users cleared successfully")
    else:
        print("❌ Failed to clear users")
        sys.exit(1)

def clear_channels():
    """Clear all allowed channels"""
    if clear_allowed_channels():
        print("✅ All channels cleared successfully")
    else:
        print("❌ Failed to clear channels")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Manage Slack Exporter access control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all allowed users and channels
  python manage_access.py --list

  # Add a user
  python manage_access.py --add-user U097LRDRB8F

  # Add a channel
  python manage_access.py --add-channel C099EEMH26N

  # Remove a user
  python manage_access.py --remove-user U097LRDRB8F

  # Remove a channel
  python manage_access.py --remove-channel C099EEMH26N

  # Clear all users
  python manage_access.py --clear-users

  # Clear all channels
  python manage_access.py --clear-channels
        """
    )

    # User management
    parser.add_argument("--add-user", help="Add a user ID to the allowed list")
    parser.add_argument("--remove-user", help="Remove a user ID from the allowed list")
    parser.add_argument("--clear-users", action="store_true", help="Clear all allowed users")

    # Channel management
    parser.add_argument("--add-channel", help="Add a channel ID to the allowed list")
    parser.add_argument("--remove-channel", help="Remove a channel ID from the allowed list")
    parser.add_argument("--clear-channels", action="store_true", help="Clear all allowed channels")

    # Display options
    parser.add_argument("--list", action="store_true", help="List all allowed users and channels")
    parser.add_argument("--users-only", action="store_true", help="List only allowed users")
    parser.add_argument("--channels-only", action="store_true", help="List only allowed channels")

    args = parser.parse_args()

    # Handle display commands
    if args.list:
        print("🔧 Slack Exporter Access Control Status")
        print("=" * 40)
        print_users()
        print()
        print_channels()
        return

    if args.users_only:
        print_users()
        return

    if args.channels_only:
        print_channels()
        return

    # Handle user management
    if args.add_user:
        add_user(args.add_user)
        return

    if args.remove_user:
        remove_user(args.remove_user)
        return

    if args.clear_users:
        confirm = input("Are you sure you want to clear all allowed users? (y/N): ")
        if confirm.lower() == 'y':
            clear_users()
        else:
            print("Operation cancelled")
        return

    # Handle channel management
    if args.add_channel:
        add_channel(args.add_channel)
        return

    if args.remove_channel:
        remove_channel(args.remove_channel)
        return

    if args.clear_channels:
        confirm = input("Are you sure you want to clear all allowed channels? (y/N): ")
        if confirm.lower() == 'y':
            clear_channels()
        else:
            print("Operation cancelled")
        return

    # If no arguments provided, show help
    parser.print_help()

if __name__ == "__main__":
    main()
