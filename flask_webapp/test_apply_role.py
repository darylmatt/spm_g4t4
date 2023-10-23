import pytest
from app import app  # Import your Flask app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_apply_role(client):
    # Define your test data
    test_data = {
        "listing_id": 22
    }

    with client.session_transaction() as sess:
        sess['Staff_ID'] = 140002
    
    headers = {
        "Content-Type": "application/json"
    }

    # Make a POST request to the route with test data
    response = client.post('/apply_role/22', data=json.dumps(test_data), headers=headers, follow_redirects=True)
    
    # Check the response status code
    assert response.status_code == 201  # You can adjust this based on your actual implementation

    # Check the response content
    data = json.loads(response.data.decode('utf-8'))
    assert "message" in data
    assert data["message"] == "Application submitted successfully"
    assert "application_id" in data
    assert "code" in data
    assert data["code"] == 201

    # Additional assertions based on your application logic

    # Clean up or additional checks as needed
