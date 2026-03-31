"""
Pytest configuration and fixtures for the Task API.

This module defines shared fixtures used across the test suite,
including the test client and sample task generators.
"""

from typing import Any, Dict, Generator, cast

import pytest
from flask.testing import FlaskClient

from app import TaskManager, app, reset_app_state


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """Create a test client for each test with fresh state."""
    app.config["TESTING"] = True
    reset_app_state()  # Clear state before each test
    with app.test_client() as client:
        yield client
    reset_app_state()  # Clean up after each test


@pytest.fixture
def task_manager() -> TaskManager:
    """Provide a fresh TaskManager for unit tests."""
    manager = TaskManager()
    return manager


@pytest.fixture
def sample_task(client: FlaskClient) -> Dict[str, Any]:
    """Create a sample task for testing."""
    response = client.post("/api/tasks", json={"title": "Test Task"})
    return cast(Dict[str, Any], response.get_json())
