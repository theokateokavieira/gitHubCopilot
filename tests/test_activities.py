import pytest

def test_get_activities(client):
    # Arrange: No special setup needed as activities are predefined
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check response status and structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success(client):
    # Arrange: Use a unique email to avoid conflicts
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act: Attempt to sign up for the activity
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Verify successful signup
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert email in result["message"]

def test_signup_duplicate(client):
    # Arrange: Sign up a student first
    email = "dup@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Attempt to sign up the same student again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Verify duplicate signup is rejected
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found(client):
    # Arrange: Use a non-existent activity name
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    
    # Act: Attempt to sign up for non-existent activity
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Verify 404 response
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success(client):
    # Arrange: First sign up a student
    email = "unreg@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Unregister the student
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert: Verify successful unregistration
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    assert email in result["message"]

def test_unregister_not_signed_up(client):
    # Arrange: Use an email not signed up for the activity
    email = "notsigned@mergington.edu"
    activity = "Chess Club"
    
    # Act: Attempt to unregister a non-participant
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert: Verify rejection of unregistration
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_activity_not_found(client):
    # Arrange: Use a non-existent activity name
    email = "test@mergington.edu"
    activity = "Nonexistent Activity"
    
    # Act: Attempt to unregister from non-existent activity
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert: Verify 404 response
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
