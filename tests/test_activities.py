"""
Tests for the GET /activities endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the API request
- Assert: Verify the response
"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    ARRANGE: No setup needed
    ACT: Request all activities
    ASSERT: Verify response contains all activities with correct structure
    """
    # ACT
    response = client.get("/activities")
    
    # ASSERT
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Verify at least one activity exists with expected structure
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_contains_chess_club(client, fresh_activities):
    """
    ARRANGE: No setup needed
    ACT: Request all activities
    ASSERT: Verify Chess Club is present with expected data
    """
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert "Chess Club" in activities
    chess_club = activities["Chess Club"]
    assert chess_club["max_participants"] == 12
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_contains_programming_class(client, fresh_activities):
    """
    ARRANGE: No setup needed
    ACT: Request all activities
    ASSERT: Verify Programming Class is present with expected data
    """
    # ACT
    response = client.get("/activities")
    activities = response.json()
    
    # ASSERT
    assert "Programming Class" in activities
    prog_class = activities["Programming Class"]
    assert prog_class["max_participants"] == 20
    assert "emma@mergington.edu" in prog_class["participants"]
    assert "sophia@mergington.edu" in prog_class["participants"]
