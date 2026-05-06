"""
Integration tests for GET /activities endpoint
"""
import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all available activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_has_correct_structure(client, reset_activities):
    """Test that each activity has the required structure"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check Chess Club structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_contains_participant_data(client, reset_activities):
    """Test that activities contain current participant data"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Chess Club should have 2 participants
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_empty_participant_list(client, reset_activities):
    """Test activities with no participants yet"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Basketball Team should have 0 participants
    basketball = data["Basketball Team"]
    assert len(basketball["participants"]) == 0
    assert basketball["max_participants"] == 15
