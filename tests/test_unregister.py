"""
Tests for the POST /activities/{activity_name}/unregister endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test preconditions
- Act: Execute the API request
- Assert: Verify the response
"""

import pytest


def test_unregister_successful(client, fresh_activities):
    """
    ARRANGE: Use an email that is currently registered for an activity
    ACT: Call unregister endpoint
    ASSERT: Verify student is removed and success message returned
    """
    # ARRANGE
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_removes_participant(client, fresh_activities):
    """
    ARRANGE: Prepare a registered participant to unregister
    ACT: Unregister the participant
    ASSERT: Verify participant is removed from the activity
    """
    # ARRANGE
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Verify participant is initially present
    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]
    
    # ACT
    client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    response = client.get("/activities")
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_not_participant_fails(client, fresh_activities):
    """
    ARRANGE: Use an email that is NOT registered for the activity
    ACT: Attempt to unregister a non-participant
    ASSERT: Verify error response with 400 status code
    """
    # ARRANGE
    email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_activity_not_found(client, fresh_activities):
    """
    ARRANGE: Use a non-existent activity name
    ACT: Attempt to unregister from the non-existent activity
    ASSERT: Verify error response with 404 status code
    """
    # ARRANGE
    email = "student@mergington.edu"
    activity_name = "NonexistentActivity"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ASSERT
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_multiple_participants(client, fresh_activities):
    """
    ARRANGE: An activity with multiple participants
    ACT: Unregister one participant, leaving others
    ASSERT: Verify only the unregistered participant is removed
    """
    # ARRANGE
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # ACT
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email_to_remove}
    )
    
    # ASSERT
    assert response.status_code == 200
    
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants


def test_unregister_then_signup_again(client, fresh_activities):
    """
    ARRANGE: A participant registered for an activity
    ACT: Unregister and then sign up again
    ASSERT: Verify participant can be re-registered after unregistering
    """
    # ARRANGE
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # ACT - unregister
    response1 = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # ACT - sign up again
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # ASSERT
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]
