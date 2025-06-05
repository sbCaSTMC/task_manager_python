from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the given Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    
    return db
