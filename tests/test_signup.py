"""
Integration tests for POST /activities/{activity_name}/signup endpoint
"""
import pytest


def test_successful_signup(client, reset_activities):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Basketball Team/signup?email=alex@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "alex@mergington.edu" in data["message"]
    assert "Basketball Team" in data["message"]


def test_signup_adds_participant_to_activity(client, reset_activities):
    """Test that signup actually adds participant to the activity"""
    # Signup
    response = client.post(
        "/activities/Basketball Team/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    basketball_participants = activities_data["Basketball Team"]["participants"]
    assert "newstudent@mergington.edu" in basketball_participants
    assert len(basketball_participants) == 1


def test_duplicate_signup_prevention(client, reset_activities):
    """Test that registering the same email twice is prevented"""
    email = "duplicate@mergington.edu"
    activity = "Basketball Team"
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_for_nonexistent_activity(client, reset_activities):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_multiple_students_can_signup(client, reset_activities):
    """Test that multiple different students can sign up for the same activity"""
    activity = "Soccer Club"
    
    # Sign up first student
    response1 = client.post(f"/activities/{activity}/signup?email=student1@mergington.edu")
    assert response1.status_code == 200
    
    # Sign up second student
    response2 = client.post(f"/activities/{activity}/signup?email=student2@mergington.edu")
    assert response2.status_code == 200
    
    # Verify both are in the activity
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    participants = activities_data[activity]["participants"]
    assert len(participants) == 2
    assert "student1@mergington.edu" in participants
    assert "student2@mergington.edu" in participants


def test_signup_preserves_existing_participants(client, reset_activities):
    """Test that new signup doesn't remove existing participants"""
    activity = "Chess Club"
    
    # Get initial participant count (should be 2)
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    assert initial_count == 2
    
    # Add new participant
    response = client.post(f"/activities/{activity}/signup?email=newchess@mergington.edu")
    assert response.status_code == 200
    
    # Verify count increased by 1
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity]["participants"])
    assert updated_count == initial_count + 1
