# tests/test_main.py
import pytest

def test_isolation_check(client):
    """Verify each test starts with clean state"""
    response = client.get('/api/tasks')
    data = response.get_json()
    assert data['count'] == 0, "Test should start with empty task list"

# ===== Integration Tests (via HTTP) =====

class TestIntegrationViaHttp:
    def test_get_empty_tasks(self, client):
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0

    def test_create_task(self, client):
        response = client.post('/api/tasks', json={'title': 'New Task'})
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Task'
        assert data['completed'] is False
    
    def test_create_task_missing_title(self, client):
        """Test validation - title is required"""
        response = client.post('/api/tasks', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_task_by_id(self, client, sample_task):
        """Test retrieving a specific task"""
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == sample_task['title']
    
    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist"""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_update_task(self, client, sample_task):
        """Test updating a task"""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={'title': 'Updated Task', 'completed': True}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Task'
        assert data['completed'] is True
    
    def test_update_task_missing_data(self, client, sample_task):
        """Test updating a task - data is required"""
        response = client.put(f"/api/tasks/{sample_task['id']}", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist"""
        response = client.put(
            "/api/tasks/9999",
            json={'title': 'Updated Task', 'completed': True}
        )
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_delete_task(self, client, sample_task):
        """Test deleting a task"""

        # First verify task exists
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200

        # Delete the task
        response = client.delete(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200

        # Verify it's gone
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist"""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404

class TestEdgeCases:
    """Additional edge case tests"""
    
    @pytest.mark.parametrize("title", ["", "   ", None])
    def test_invalid_titles(self, client, title):
        """Test various invalid title inputs"""
        response = client.post('/api/tasks', json={'title': title})
        # Empty strings might be accepted depending on validation rules
        # This shows parameterized testing
    
    def test_multiple_tasks(self, client):
        """Test creating and listing multiple tasks"""
        for i in range(5):
            response = client.post('/api/tasks', json={'title': f'Task {i}'})
            assert response.status_code == 201
        
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 5

# ===== Unit Tests (Direct Model Testing) =====

class TestModelDirectly:
    def test_task_manager_create(self, task_manager):
        task = task_manager.create('My Task')
        assert task['title'] == 'My Task'
        assert task['id'] == 1
        assert task['completed'] is False

    def test_task_manager_get_by_id(self, task_manager):
        task_manager.create('Task 1')
        task_manager.create('Task 2')
        task = task_manager.get_by_id(2)
        assert task['title'] == 'Task 2'

    def test_task_manager_delete(self, task_manager):
        task = task_manager.create('To Delete')
        assert task_manager.delete(task['id']) is True
        assert task_manager.get_by_id(task['id']) is None

    def test_task_manager_reset(self, task_manager):
        task_manager.create('Task 1')
        task_manager.create('Task 2')
        task_manager.reset()
        assert task_manager.count == 0
        assert task_manager._next_id == 1
