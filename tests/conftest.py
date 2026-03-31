import pytest
from app import app, reset_app_state, TaskManager

@pytest.fixture
def client():
    """Create a test client for each test with fresh state"""
    app.config['TESTING'] = True
    reset_app_state()  # Clear state before each test
    with app.test_client() as client:
        yield client
    reset_app_state()  # Clean up after each test

@pytest.fixture
def task_manager():
    """Provide a fresh TaskManager for unit tests"""
    manager = TaskManager()
    return manager

@pytest.fixture
def sample_task(client):
    """Create a sample task for testing"""
    response = client.post('/api/tasks', json={'title': 'Test Task'})
    return response.get_json()
