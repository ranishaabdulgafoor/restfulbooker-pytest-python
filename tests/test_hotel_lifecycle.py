import pytest
from api_client import ApiClient
from tests.schemas import BOOKING_SCHEMA
from jsonschema import validate
from utils.logger import log_failure_transaction

# Initialize our dynamic variables and client engine instances
client = ApiClient()
admin_token = None
booking_id = None

def test_01_ping_server():
    """Verify backend system status and server availability."""
    response = client.get("/ping")
    try:
        assert response.status_code == 201
        assert response.text == "Created"
    except AssertionError:
        log_failure_transaction("test_01_ping_server", response)
        raise

def test_02_generate_token():
    """Authenticate administrative session credentials to extract authorization tokens."""
    global admin_token
    payload = {"username": "admin", "password": "password123"}
    response = client.post("/auth", json_data=payload)
    
    try:
        assert response.status_code == 200       
        response_data = response.json()
        assert "token" in response_data
        admin_token = response_data["token"]
        print(f"\n[SUCCESS] Extracted Dynamic Token: {admin_token}")
    except (AssertionError, Exception):
        log_failure_transaction("test_02_generate_token", response, payload)
        raise

def test_03_create_booking():
    """Create a new guest record transaction and extract the unique resource key."""
    global booking_id
    payload = {
        "firstname": "Alex", "lastname": "Tester", "totalprice": 250, "depositpaid": True,
        "bookingdates": {"checkin": "2030-01-01", "checkout": "2030-01-10"}, "additionalneeds": "Breakfast"
    }
    response = client.post("/booking", json_data=payload)
    
    try:
        assert response.status_code == 200        
        response_data = response.json()
        assert "bookingid" in response_data
        booking_id = response_data["bookingid"]
        
        # Guide Constraint Match: Validate structural data schema integrity
        validate(instance=response_data["booking"], schema=BOOKING_SCHEMA)
        print(f"\n[SUCCESS] Generated Live Booking ID: {booking_id}")
    except (AssertionError, Exception):
        log_failure_transaction("test_03_create_booking", response, payload)
        raise

def test_04_get_booking():
    """Query guest record database and validate state tracking integrity."""
    response = client.get(f"/booking/{booking_id}")

    try:
        assert response.status_code == 200     
        response_data = response.json()
        assert response_data["firstname"] == "Alex"
        assert response_data["lastname"] == "Tester"
        
        # Guide Constraint Match: Validate schema payload structure contract matching
        validate(instance=response_data, schema=BOOKING_SCHEMA)
        print(f"\n[SUCCESS] Verified Guest State inside Room Ledger: {response_data['firstname']}")
    except (AssertionError, Exception):
        log_failure_transaction("test_04_get_booking", response)
        raise

def test_05_update_booking():
    """Execute complete resource record override utilizing session cookie permissions."""
    headers = {"Cookie": f"token={admin_token}", "Accept": "application/json"}
    payload = {
        "firstname": "Alex", "lastname": "Tester", "totalprice": 350, "depositpaid": True,
        "bookingdates": {"checkin": "2030-01-01", "checkout": "2030-01-10"}, "additionalneeds": "Dinner"
    }
    response = client.put(f"/booking/{booking_id}", json_data=payload, headers=headers)
    
    try:
        assert response.status_code == 200     
        response_data = response.json()
        assert response_data["additionalneeds"] == "Dinner"
        assert response_data["totalprice"] == 350
        validate(instance=response_data, schema=BOOKING_SCHEMA)
        print(f"\n[SUCCESS] PUT Overwrite Verified: Package updated to {response_data['additionalneeds']}")
    except (AssertionError, Exception):
        log_failure_transaction("test_05_update_booking", response, payload)
        raise

def test_06_partial_update():
    """Surgically modify discrete attributes inside a target entity using PATCH."""
    headers = {"Cookie": f"token={admin_token}", "Accept": "application/json"}
    payload = {"firstname": "Ranisha"}
    response = client.patch(f"/booking/{booking_id}", json_data=payload, headers=headers)
    
    try:
        assert response.status_code == 200      
        response_data = response.json()
        assert response_data["firstname"] == "Ranisha"
        validate(instance=response_data, schema=BOOKING_SCHEMA)
        print(f"\n[SUCCESS] PATCH Edit Verified: Name updated to {response_data['firstname']}")
    except (AssertionError, Exception):
        log_failure_transaction("test_06_partial_update", response, payload)
        raise

def test_07_delete_booking():
    """Purge target guest reservation state from the backend server."""
    headers = {"Cookie": f"token={admin_token}"}
    response = client.delete(f"/booking/{booking_id}", headers=headers)
    
    try:
        assert response.status_code == 201
        assert response.text == "Created"
        print(f"\n[SUCCESS] DELETE Executed: Record {booking_id} wiped from ledger database")
    except AssertionError:
        log_failure_transaction("test_07_delete_booking", response)
        raise

def test_08_ghost_check():
    """Validate teardown lifecycle operations by verifying structural entity absence."""
    response = client.get(f"/booking/{booking_id}")
    try:
        assert response.status_code == 404
        assert response.text == "Not Found"
        print(f"\n[SUCCESS] Ghost Check Passed: Verified 404 and string response matches '{response.text}'")
    except AssertionError:
        log_failure_transaction("test_08_ghost_check", response)
        raise

# =====================================================================
# NEGATIVE TEST SUITE BOUNDS
# =====================================================================

def test_09_create_booking_missing_required_fields():
    """Verify server rejects data payloads missing mandatory field criteria."""
    response = client.post("/booking", json_data={})
    try:
        assert response.status_code in [400, 500]
    except AssertionError:
        log_failure_transaction("test_09_create_booking_missing_required_fields", response, {})
        raise

def test_10_update_booking_with_invalid_token():
    """Verify security controls intercept unauthenticated object mutations."""
    headers = {"Cookie": "token=INVALID_EXPIRED_OR_FAKE_TOKEN", "Accept": "application/json"}
    payload = {
        "firstname": "Hacker", "lastname": "Tester", "totalprice": 0, "depositpaid": False,
        "bookingdates": {"checkin": "2030-01-01", "checkout": "2030-01-10"}, "additionalneeds": "None"
    }
    response = client.put(f"/booking/{booking_id}", json_data=payload, headers=headers)
    try:
        assert response.status_code == 403
        assert response.text == "Forbidden"
    except AssertionError:
        log_failure_transaction("test_10_update_booking_with_invalid_token", response, payload)
        raise

def test_11_get_booking_by_invalid_id_format():
    """Verify data routing controls handle non-existent alphanumeric query arguments."""
    response = client.get("/booking/abc-999-xyz")
    try:
        assert response.status_code == 404
    except AssertionError:
        log_failure_transaction("test_11_get_booking_by_invalid_id_format", response)
        raise
