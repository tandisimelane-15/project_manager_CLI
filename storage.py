import json
import os
from models.user import User
from models.admin_user import AdminUser

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def save_users(users):
    
    data = {"users": [user.to_dict() for user in users]}
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except OSError as e:
        print(f"Error saving data: {e}")
        raise

def user_from_dict(user_data):
    """
    Rebuild the correct user type from saved JSON data.
    """
    if user_data.get("is_admin", False):
        return AdminUser.from_dict(user_data)

    return User.from_dict(user_data)

def load_users():
    """
    Reads data.json and rebuilds User object
    Returns an empty list if the file doesn't exist yet or is corrupted,
    so a bad/missing file doesn't crash the whole program.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Warning: could not read data file ({e}). Starting fresh.")
        return []

    return [
    user_from_dict(user_data)
    for user_data in data.get("users", [])
]