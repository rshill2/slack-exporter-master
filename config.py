import os
import json
from typing import Set, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration file paths
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
ALLOWED_USERS_FILE = os.path.join(CONFIG_DIR, "allowed_users.json")
ALLOWED_CHANNELS_FILE = os.path.join(CONFIG_DIR, "allowed_channels.json")

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

def load_json_file(filepath: str, default: List = None) -> Set[str]:
    """Load a JSON file containing a list of strings, return as a set"""
    if default is None:
        default = []
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('items', default))
        else:
            # Create file with default data
            save_json_file(filepath, default)
            return set(default)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {filepath}: {e}")
        return set(default)

def save_json_file(filepath: str, items: List[str]) -> bool:
    """Save a list of strings to a JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({'items': list(items)}, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {filepath}: {e}")
        return False

def get_allowed_users() -> Set[str]:
    """Get the set of allowed user IDs"""
    return load_json_file(ALLOWED_USERS_FILE, default=[])

def get_allowed_channels() -> Set[str]:
    """Get the set of allowed channel IDs"""
    return load_json_file(ALLOWED_CHANNELS_FILE, default=[])

def add_allowed_user(user_id: str) -> bool:
    """Add a user ID to the allowed users list"""
    if not user_id.startswith('U'):
        print(f"Invalid user ID format: {user_id}. Must start with 'U'")
        return False
    
    users = get_allowed_users()
    users.add(user_id)
    return save_json_file(ALLOWED_USERS_FILE, list(users))

def remove_allowed_user(user_id: str) -> bool:
    """Remove a user ID from the allowed users list"""
    users = get_allowed_users()
    if user_id in users:
        users.remove(user_id)
        return save_json_file(ALLOWED_USERS_FILE, list(users))
    return False

def add_allowed_channel(channel_id: str) -> bool:
    """Add a channel ID to the allowed channels list"""
    if not channel_id.startswith('C'):
        print(f"Invalid channel ID format: {channel_id}. Must start with 'C'")
        return False
    
    channels = get_allowed_channels()
    channels.add(channel_id)
    return save_json_file(ALLOWED_CHANNELS_FILE, list(channels))

def remove_allowed_channel(channel_id: str) -> bool:
    """Remove a channel ID from the allowed channels list"""
    channels = get_allowed_channels()
    if channel_id in channels:
        channels.remove(channel_id)
        return save_json_file(ALLOWED_CHANNELS_FILE, list(channels))
    return False

def is_user_allowed(user_id: str) -> bool:
    """Check if a user ID is in the allowed users list"""
    allowed_users = get_allowed_users()
    return user_id in allowed_users

def is_channel_allowed(channel_id: str) -> bool:
    """Check if a channel ID is in the allowed channels list"""
    allowed_channels = get_allowed_channels()
    return channel_id in allowed_channels

def list_allowed_users() -> List[str]:
    """Get a list of all allowed user IDs"""
    return sorted(list(get_allowed_users()))

def list_allowed_channels() -> List[str]:
    """Get a list of all allowed channel IDs"""
    return sorted(list(get_allowed_channels()))

def clear_allowed_users() -> bool:
    """Clear all allowed users"""
    return save_json_file(ALLOWED_USERS_FILE, [])

def clear_allowed_channels() -> bool:
    """Clear all allowed channels"""
    return save_json_file(ALLOWED_CHANNELS_FILE, [])

# Initialize with example data if files don't exist
def initialize_example_data():
    """Initialize with example user and channel if no data exists"""
    users = get_allowed_users()
    channels = get_allowed_channels()
    
    if not users:
        add_allowed_user("U097LRDRB8F")
        print("Added example user: U097LRDRB8F")
    
    if not channels:
        add_allowed_channel("C099EEMH26N")
        print("Added example channel: C099EEMH26N")

# Run initialization
initialize_example_data()
