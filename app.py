import os
import sys
from datetime import datetime, timezone
from flask import Flask, render_template

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import SECRET_KEY, DEBUG
from database import init_db, db
from routes.tasks import tasks_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config')
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(tasks_bp, url_prefix='')
    
    # Add current year to all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    app.run(debug=DEBUG)
