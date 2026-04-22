"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for all tests, including:
- FastAPI TestClient instance
- Fresh activities data reset before each test
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making test API requests.
    
    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def fresh_activities(client):
    """
    Resets activities to initial state before each test.
    
    This fixture ensures test isolation by resetting the in-memory
    activities database to a known state before each test runs.
    
    Yields:
        dict: Reference to the activities dictionary in fresh state
    """
    # Store original state
    original_activities = copy.deepcopy(activities)
    
    yield activities
    
    # Reset to original state after test
    activities.clear()
    activities.update(original_activities)
