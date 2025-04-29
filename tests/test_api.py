import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_receipt_process_and_points(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
            { "shortDescription": "Emils Cheese Pizza", "price": "12.25" },
            { "shortDescription": "Knorr Creamy Chicken", "price": "1.26" },
            { "shortDescription": "Doritos Nacho Cheese", "price": "3.35" },
            { "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00" }
        ],
        "total": "35.35"
    }

    # POST request to process receipt
    post_response = client.post("/receipts/process", json=receipt)
    assert post_response.status_code == 200
    data = post_response.get_json()
    assert "id" in data
    receipt_id = data["id"]

    # GET request to retrieve points
    get_response = client.get(f"/receipts/{receipt_id}/points")
    assert get_response.status_code == 200
    points_data = get_response.get_json()
    assert "points" in points_data
    assert isinstance(points_data["points"], int)

def test_process_receipt_with_no_json(client):
    response = client.post("/receipts/process")
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_process_receipt_with_dummy_data(client):
    response = client.post(
        "/receipts/process",
        data="hello this is not json",
        content_type="text/plain"
    )
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_get_points_receipt_not_found(client):
    fake_id = "non-existent-id"
    response = client.get(f"/receipts/{fake_id}/points")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No receipt found for that ID."

def test_post_receipt_missing_field(client):
    # Missing "items"
    receipt = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-05-10",
        "purchaseTime": "13:45",
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_bad_total_format(client):
    # Bad total (not matching regex)
    receipt = {
        "retailer": "M&M Market",
        "purchaseDate": "2022-05-10",
        "purchaseTime": "13:45",
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_get_points_invalid_id_format(client):
    bad_id = "bad id with spaces"
    response = client.get(f"/receipts/{bad_id}/points")
    assert response.status_code == 404
    assert response.get_json() == {"error": "No receipt found for that ID."}

def test_post_receipt_invalid_retailer_characters(client):
    # Retailer name has invalid special character (!)
    receipt = {
        "retailer": "Target!",  # "!" not allowed
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_purchase_date_format(client):
    # Purchase date in wrong format (DD-MM-YYYY instead of YYYY-MM-DD)
    receipt = {
        "retailer": "Target",
        "purchaseDate": "01-01-2022",  # wrong
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_purchase_time_format(client):
    # Purchase time in wrong format (single digit hour)
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "9:1",  # wrong
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_item_short_description(client):
    # Item shortDescription has invalid special character
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Mountain Dew 12PK!", "price": "6.49"}],  # "!" not allowed
        "total": "6.49"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_item_price_format(client):
    # Item price missing cents
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6"}],  # wrong format
        "total": "6.00"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_month_over_12(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-13-01",  # Invalid month (13)
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_day_over_31(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-12-32",  # Invalid day (32)
        "purchaseTime": "13:01",
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_hour_over_23(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-12-31",
        "purchaseTime": "25:00",  # Invalid hour (25)
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}

def test_post_receipt_invalid_minute_over_59(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-12-31",
        "purchaseTime": "23:61",  # Invalid minute (61)
        "items": [{"shortDescription": "Item One", "price": "5.99"}],
        "total": "5.99"
    }
    response = client.post("/receipts/process", json=receipt)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The receipt is invalid."}