import random
from playwright.sync_api import APIRequestContext

def test_get_booking(api_context: APIRequestContext):
    response = api_context.get("/booking")
    assert response.status == 200
    assert isinstance(response.json(), list)

def test_get_specific_booking_id(api_context: APIRequestContext):
    response = api_context.get("/booking")
    assert response.status == 200
    bookings = response.json()
    assert len(bookings) > 0, "No bookings available to test"
    booking_id = random.choice(bookings)["bookingid"]
    print(f"Randomly selected booking ID: {booking_id}")
    booking_response = api_context.get(f"/booking/{booking_id}")
    assert booking_response.status == 200

def test_create_booking(api_context: APIRequestContext, load_payload):
    payload = load_payload("create_booking.json")
    response = api_context.post("/booking", data=payload)
    assert response.status == 200
    response_data = response.json()
    booking_id = response_data["bookingid"]
    booking = response_data["booking"]
    assert booking == payload

def test_update_booking(api_context: APIRequestContext, load_payload, auth_headers, created_booking):
    # Step 1: Create a booking using create_booking.json
    booking_id = created_booking

    # Step 2: Update booking
    update_payload = load_payload("update_booking.json")

    update_response = api_context.put(
        f"/booking/{booking_id}",
        data=update_payload,
        headers=auth_headers
    )

    assert update_response.status == 200
    response_data = update_response.json()
    assert response_data == update_payload

def test_partial_update_booking(api_context: APIRequestContext, load_payload, auth_headers, created_booking):
    # Step 1: Create a booking using create_booking.json
    booking_id = created_booking

    # Step 2: Send PATCH request with authentication headers
    patch_payload = load_payload("patch_booking.json")
    patch_response = api_context.patch(f"/booking/{booking_id}", data=patch_payload, headers=auth_headers)
    assert patch_response.status == 200
    updated_booking = patch_response.json()
    assert updated_booking["firstname"] == patch_payload["firstname"]
    assert updated_booking["totalprice"] == patch_payload["totalprice"]

def test_delete_booking(api_context: APIRequestContext, auth_headers, created_booking):
    # Step 1: Create a booking using create_booking.json
    booking_id = created_booking

    # Step 2: Delete booking
    response = api_context.delete(f"/booking/{booking_id}", headers=auth_headers)
    delete_message = response.text()
    assert response.status == 201
    assert delete_message == "Created"

    # Step 3: Verify booking no longer exists
    get_response = api_context.get(f"/booking/{booking_id}")
    assert get_response.status == 404