from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.task import Task
from utils.calculator import Calculator
from database import db

# Create a Blueprint for task routes
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """Display all tasks."""
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """Add a new task."""
    title = request.form.get('title', '').strip()
    
    if not title:
        flash('Task title cannot be empty', 'error')
    else:
        task = Task(title=title)
        task.save()
        flash('Task added successfully!', 'success')
    
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task by ID."""
    task = Task.get_by_id(task_id)
    task.delete()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.index'))

# API endpoints for future AJAX functionality
@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks as JSON."""
    tasks = Task.get_all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """Toggle task completion status."""
    task = Task.get_by_id(task_id)
    task.completed = not task.completed
    task.save()
    return jsonify({'success': True, 'completed': task.completed})

@tasks_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """
    Calculate the result of a mathematical expression.
    
    Expected JSON payload:
    {
        "expression": "2 + 2 * 3"
    }
    
    Returns:
        JSON response with the result or error message
    """
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({
            'success': False,
            'error': 'No expression provided',
            'expression': ''
        }), 400
    
    # Calculate the result using our Calculator utility
    result = Calculator.calculate(data['expression'])
    return jsonify(result)
