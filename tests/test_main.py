# tests/test_main.py
"""
Integration and unit tests for the Task API.

This module contains tests for task CRUD operations using both
the HTTP client and direct model interaction.
"""

from typing import Any, Dict, Optional, Union

import pytest
from flask.testing import FlaskClient

from app.models import TaskManager


def test_isolation_check(client: FlaskClient) -> None:
    """Verify each test starts with clean state."""
    response = client.get("/api/tasks")
    data = response.get_json()
    assert data["count"] == 0, "Test should start with empty task list."


class TestIntegrationViaHttp:
    """Integration Tests (via HTTP)."""

    def test_get_empty_tasks(self, client: FlaskClient) -> None:
        """Test retrieving tasks when the list is empty."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 0

    def test_create_task(self, client: FlaskClient) -> None:
        """Test creating a new task with a valid title."""
        response = client.post("/api/tasks", json={"title": "New Task"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "New Task"
        assert data["completed"] is False

    def test_create_task_missing_title(self, client: FlaskClient) -> None:
        """Test validation - title is required."""
        response = client.post("/api/tasks", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_get_task_by_id(
        self, client: FlaskClient, sample_task: Dict[str, Any]
    ) -> None:
        """Test retrieving a specific task."""
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == sample_task["title"]

    def test_get_nonexistent_task(self, client: FlaskClient) -> None:
        """Test getting a task that doesn't exist."""
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_update_task(
        self, client: FlaskClient, sample_task: Dict[str, Any]
    ) -> None:
        """Test updating a task."""
        response = client.put(
            f"/api/tasks/{sample_task['id']}",
            json={"title": "Updated Task", "completed": True},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Updated Task"
        assert data["completed"] is True

    def test_update_task_missing_data(
        self, client: FlaskClient, sample_task: Dict[str, Any]
    ) -> None:
        """Test updating a task - data is required."""
        response = client.put(f"/api/tasks/{sample_task['id']}", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_nonexistent_task(self, client: FlaskClient) -> None:
        """Test updating a task that doesn't exist."""
        response = client.put("/api/tasks/9999", json={"title": "Task"})
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_delete_task(
        self, client: FlaskClient, sample_task: Dict[str, Any]
    ) -> None:
        """Test deleting a task."""
        # First verify task exists
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200

        # Delete the task
        response = client.delete(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 200

        # Verify it's gone
        response = client.get(f"/api/tasks/{sample_task['id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_task(self, client: FlaskClient) -> None:
        """Test deleting a task that doesn't exist."""
        response = client.delete("/api/tasks/9999")
        assert response.status_code == 404


class TestEdgeCases:
    """Additional edge case tests."""

    @pytest.mark.parametrize("title", ["", "   ", None])
    def test_invalid_titles(
        self, client: FlaskClient, title: Union[str, None]
    ) -> Optional[None]:
        """Test various invalid title inputs."""
        response = client.post("/api/tasks", json={"title": title})
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == title

    def test_multiple_tasks(self, client: FlaskClient) -> None:
        """Test creating and listing multiple tasks."""
        for i in range(5):
            response = client.post("/api/tasks", json={"title": f"Task {i}"})
            assert response.status_code == 201

        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.get_json()
        assert data["count"] == 5


class TestModelDirectly:
    """Unit Tests (Direct Model Testing)."""

    def test_task_manager_create(self, task_manager: TaskManager) -> None:
        """Test creating a task via the TaskManager model."""
        task = task_manager.create("My Task")
        assert task["title"] == "My Task"
        assert task["id"] == 1
        assert task["completed"] is False

    def test_task_manager_get_by_id(self, task_manager: TaskManager) -> None:
        """Test retrieving a task by ID via the TaskManager model."""
        task_manager.create("Task 1")
        task_manager.create("Task 2")
        task = task_manager.get_by_id(2)
        assert task is not None
        assert task["title"] == "Task 2"

    def test_task_manager_delete(self, task_manager: TaskManager) -> None:
        """Test deleting a task via the TaskManager model."""
        task = task_manager.create("To Delete")
        assert task_manager.delete(task["id"]) is True
        assert task_manager.get_by_id(task["id"]) is None

    def test_task_manager_reset(self, task_manager: TaskManager) -> None:
        """Test resetting the TaskManager state."""
        task_manager.create("Task 1")
        task_manager.create("Task 2")
        task_manager.reset()
        assert task_manager.count == 0
        assert task_manager._next_id == 1
