import uuid
from dateutil import parser as date_parser


def generate_id():
    """Generate a short unique ID for users, projects, or tasks."""
    return str(uuid.uuid4())[:8]


def validate_date(date_str):
    """
    Validates and normalizes a due-date string using python-dateutil.
    Returns the date in YYYY-MM-DD format, or None if blank.
    Raises ValueError if the string can't be parsed as a date at all.
    """
    if not date_str:
        return None
    parsed = date_parser.parse(date_str)
    return parsed.strftime("%Y-%m-%d")