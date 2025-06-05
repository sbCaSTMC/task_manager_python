from datetime import datetime
from database import db

class Task(db.Model):
    """Task model for the task management application."""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, title, description=None, category=None, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def to_dict(self):
        """Convert task object to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def get_all(cls):
        """Get all tasks."""
        return cls.query.order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_id(cls, task_id):
        """Get a task by ID."""
        return cls.query.get_or_404(task_id)
    
    def save(self):
        """Save the current task to the database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the current task from the database."""
        db.session.delete(self)
        db.session.commit()
        return True
