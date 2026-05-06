"""
Integration tests for DELETE /activities/{activity_name}/participants/{email} endpoint
"""
import pytest


def test_successful_participant_removal(client, reset_activities):
    """Test successful removal of a participant from an activity"""
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert "Removed" in data["message"]


def test_removal_updates_participant_list(client, reset_activities):
    """Test that removal actually removes participant from activity"""
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    
    # Verify participant exists before removal
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]
    
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    
    # Verify participant is removed
    updated_response = client.get("/activities")
    assert email not in updated_response.json()[activity]["participants"]


def test_removal_of_nonexistent_participant(client, reset_activities):
    """Test removal of a participant not in the activity"""
    activity = "Basketball Team"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_removal_from_nonexistent_activity(client, reset_activities):
    """Test removal from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/participants/student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_removal_decreases_participant_count(client, reset_activities):
    """Test that removal decreases the participant count correctly"""
    activity = "Programming Class"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity]["participants"])
    
    email_to_remove = "emma@mergington.edu"
    
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email_to_remove}")
    assert response.status_code == 200
    
    # Verify count decreased by 1
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity]["participants"])
    assert updated_count == initial_count - 1


def test_removal_preserves_other_participants(client, reset_activities):
    """Test that removing one participant doesn't affect others"""
    activity = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Remove one participant
    response = client.delete(f"/activities/{activity}/participants/{email_to_remove}")
    assert response.status_code == 200
    
    # Verify other participant is still there
    updated_response = client.get("/activities")
    participants = updated_response.json()[activity]["participants"]
    assert email_to_remove not in participants
    assert email_to_keep in participants


def test_signup_then_removal_workflow(client, reset_activities):
    """Test complete workflow: signup, verify, then remove"""
    activity = "Art Club"
    email = "artlover@mergington.edu"
    
    # Sign up
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    
    # Verify added
    check_response = client.get("/activities")
    assert email in check_response.json()[activity]["participants"]
    
    # Remove
    remove_response = client.delete(f"/activities/{activity}/participants/{email}")
    assert remove_response.status_code == 200
    
    # Verify removed
    final_response = client.get("/activities")
    assert email not in final_response.json()[activity]["participants"]
