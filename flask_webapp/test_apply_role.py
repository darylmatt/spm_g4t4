import pytest
from app import app 
import json
import logging

application_id = None

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test-specific cleanup logic
def clean_up_application(client):
    global application_id
    if application_id is not None:
        # Make a DELETE request to the route to delete the application
        response = client.delete(f'/delete_application/{application_id}', follow_redirects=True)
        assert response.status_code == 200

# Define a fixture that uses the test-specific cleanup logic
@pytest.fixture
def cleanup_application(request, client):
    # This fixture will be automatically used before and after each test function
    request.addfinalizer(lambda: clean_up_application(client))

# Test creating a new application
def test_apply_role(self):
        global application_id
        # Define your test data
        test_data = {
            "listing_id": 17
        }

        with self.client.session_transaction() as sess:
            sess['Staff_ID'] = 140002
            sess['Role'] = 2

        headers = {
            "Content-Type": "application/json"
        }

        # Make a POST request to the route with test data
        response = self.client.post('/apply_role/17', data=json.dumps(test_data), headers=headers, follow_redirects=True)

        # Check the response status code
        self.assertEqual(response.status_code, 201)  # You can adjust this based on your actual implementation

        # Check the response content
        data = json.loads(response.data.decode('utf-8'))
        application_id = data.get("application_id")
        logging.info(f"Application ID in application: {application_id}")
        
# Test trying to apply to same role again
def test_apply_existing_role(client):
    global application_id
    # Define your test data
    test_data = {
        "listing_id": 2
    }

    with client.session_transaction() as sess:
        sess['Staff_ID'] = 140002
        sess['Role'] = 2

    headers = {
        "Content-Type": "application/json"
    }

    # Make a POST request to the route with test data
    response = client.post('/apply_role/2', data=json.dumps(test_data), headers=headers, follow_redirects=True)

    # Check the response status code
    assert response.status_code == 400  # You can adjust this based on your actual implementation

    expected_error_message = "You have already applied to this role"
    assert expected_error_message in response.get_json()['error']

# Test applying to a role that is already closed
def test_apply_closed_role(client):
    global application_id
    # Define your test data
    test_data = {
        "listing_id": 18  # Replace with a valid listing ID for an open role
    }

    with client.session_transaction() as sess:
        sess['Staff_ID'] = 140002
        sess['Role'] = 2

    headers = {
        "Content-Type": "application/json"
    }

    # Make a POST request to the route with test data
    response = client.post('/apply_role/18', data=json.dumps(test_data), headers=headers, follow_redirects=True)
    
    # Check the response status code
    assert response.status_code == 411  # You can adjust this based on your actual implementation

    expected_error_message = "Role listing is closed or not yet open for applications"
    assert expected_error_message in response.get_json()['error']