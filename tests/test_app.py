import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_delete_participant():
    # Sign up a new participant
    email = "testuser@example.com"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    # Check participant is added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]
    # Remove participant
    del_resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert del_resp.status_code == 200
    # Check participant is removed
    get_resp2 = client.get("/activities")
    assert email not in get_resp2.json()[activity]["participants"]

def test_signup_duplicate():
    email = "duplicate@example.com"
    activity = "Chess Club"
    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Duplicate signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student is already signed up"
    # Cleanup
    client.delete(f"/activities/{activity}/participants/{email}")

def test_delete_nonexistent_participant():
    activity = "Chess Club"
    email = "notfound@example.com"
    resp = client.delete(f"/activities/{activity}/participants/{email}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found"

def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"

def test_delete_nonexistent_activity():
    resp = client.delete("/activities/Nonexistent/participants/foo@bar.com")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
