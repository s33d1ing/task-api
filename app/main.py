from flask import Flask, jsonify, request
from .models import TaskManager

app = Flask(__name__)

# Create a shared TaskManager instance
task_manager = TaskManager()

def reset_app_state():
    """Reset state for testing"""
    task_manager.reset()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = task_manager.get_all()
    return jsonify({'tasks': tasks, 'count': len(tasks)}), 200

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = task_manager.get_by_id(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    task = task_manager.create(data['title'])
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    task = task_manager.update(task_id, data)
    if task:
        return jsonify(task), 200

    return jsonify({'error': 'Task not found'}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    if task_manager.delete(task_id):
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404
