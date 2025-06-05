from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.task import Task
from utils.calculator import Calculator
from database import db

# タスク関連のルート用のBlueprintを作成
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def index():
    """すべてのタスクを表示する。"""
    tasks = Task.get_all()
    return render_template('index.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """新しいタスクを追加する。"""
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
    """IDでタスクを削除する。"""
    task = Task.get_by_id(task_id)
    task.delete()
    flash('タスクを削除しました!', 'success')
    return redirect(url_for('tasks.index'))

# AJAX機能のためのAPIエンドポイント
@tasks_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """すべてのタスクをJSON形式で取得する。"""
    tasks = Task.get_all()
    return jsonify([task.to_dict() for task in tasks])

@tasks_bp.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """タスクの完了状態を切り替える。"""
    task = Task.get_by_id(task_id)
    task.completed = not task.completed
    task.save()
    return jsonify({'success': True, 'completed': task.completed})

@tasks_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """
    数式の計算結果を取得する。
    
    期待されるJSONペイロード:
    {
        "expression": "2 + 2 * 3"
    }
    
    戻り値:
        結果またはエラーメッセージを含むJSONレスポンス
    """
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({
            'success': False,
            'error': 'No expression provided',
            'expression': ''
        }), 400
    
    # Calculatorユーティリティを使用して結果を計算
    result = Calculator.calculate(data['expression'])
    return jsonify(result)
