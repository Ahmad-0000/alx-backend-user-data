"""
Loading the database
"""

from models.user import User


User.load_from_file()
