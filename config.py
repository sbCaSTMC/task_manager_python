import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'task_manager.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret key for session management
SECRET_KEY = 'your-secret-key-here'  # Change this in production

# Debug mode (set to False in production)
DEBUG = True
