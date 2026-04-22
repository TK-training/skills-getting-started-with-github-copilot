"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the API request
- Assert: Verify the response
"""

import pytest


def test_signup_successful(client, fresh_activities):
    """
    ARRANGE: Prepare email and activity that exists but student is not signed up
    ACT: Call signup endpoint
    ASSERT: Verify student is added to participants and success message returned
    """
    # ARRANGE
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_adds_participant_to_activity(client, fresh_activities):
    """
    ARRANGE: Prepare new student email for Chess Club
    ACT: Sign up the student
    ASSERT: Verify student appears in the activity's participants list
    """
    # ARRANGE
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # ACT
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # ASSERT
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_already_registered_fails(client, fresh_activities):
    """
    ARRANGE: Use an email already registered for Chess Club
    ACT: Attempt to sign up the same student again
    ASSERT: Verify error response with 400 status code
    """
    # ARRANGE
    email = "michael@mergington.edu"  # Already in Chess Club
    activity_name = "Chess Club"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client, fresh_activities):
    """
    ARRANGE: Use a non-existent activity name
    ACT: Attempt to sign up for the non-existent activity
    ASSERT: Verify error response with 404 status code
    """
    # ARRANGE
    email = "student@mergington.edu"
    activity_name = "NonexistentActivity"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_students_same_activity(client, fresh_activities):
    """
    ARRANGE: Sign up two different students for the same activity
    ACT: Sign up first student, then second student
    ASSERT: Verify both students are in the participants list
    """
    # ARRANGE
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    activity_name = "Programming Class"
    
    # ACT
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # ASSERT
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    response = client.get("/activities")
    activities = response.json()
    participants = activities[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants
