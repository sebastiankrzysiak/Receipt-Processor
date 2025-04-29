from services.points import calculate_points

# ----------------------------------------------------------------------------------------
# Official Example Tests from the Fetch Take-Home Assignment README
# These are provided by the company as reference and should always pass as-is.
# ----------------------------------------------------------------------------------------

def test_readme_target_receipt():
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
            },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
            },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
            },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
            },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
            }
        ],
        "total": "35.35"
    }

    assert calculate_points(receipt) == 28

def test_readme_m_and_m_receipt():
    receipt = {
        "retailer": "M&M Corner Market",
        "purchaseDate": "2022-03-20",
        "purchaseTime": "14:33",
        "items": [
          {
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          },{
            "shortDescription": "Gatorade",
            "price": "2.25"
          }
        ],
        "total": "9.00"
    }

    assert calculate_points(receipt) == 109


# ----------------------------------------------------------------------------------------
# Rule 1 Tests: Alphanumeric Characters in Retailer Name
# ----------------------------------------------------------------------------------------

def test_rule1_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule1_medium():
    receipt = {
        "retailer": "7-Eleven",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 88


def test_rule1_hard():
    receipt = {
        "retailer": "W@lmart+",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 87


# ----------------------------------------------------------------------------------------
# Rule 2 Tests: 50 Points for Round Dollar Amounts (e.g., "20.00")
# ----------------------------------------------------------------------------------------

def test_rule2_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule2_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.99"}
        ],
        "total": "1.99"
    }

    assert calculate_points(receipt) == 9


def test_rule2_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.01"}
        ],
        "total": "1.01"
    }

    assert calculate_points(receipt) == 9


# ----------------------------------------------------------------------------------------
# Rule 3 Tests: 25 Points for Totals That Are Multiples of 0.25
# ----------------------------------------------------------------------------------------

def test_rule3_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "0.25"}
        ],
        "total": "0.25"
    }

    assert calculate_points(receipt) == 34


def test_rule3_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "2.75"}
        ],
        "total": "2.75"
    }

    assert calculate_points(receipt) == 34


def test_rule3_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.26"}
        ],
        "total": "1.26"
    }

    assert calculate_points(receipt) == 9


# ----------------------------------------------------------------------------------------
# Rule 4 Tests: 5 Points for Every 2 Items on the Receipt
# ----------------------------------------------------------------------------------------

def test_rule4_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item A", "price": "1.00"},
            {"shortDescription": "Item B", "price": "1.00"}
        ],
        "total": "2.00"
    }

    assert calculate_points(receipt) == 91


def test_rule4_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "One", "price": "1.00"},
            {"shortDescription": "Two", "price": "1.00"},
            {"shortDescription": "Three", "price": "1.00"},
            {"shortDescription": "Four", "price": "1.00"},
            {"shortDescription": "Five", "price": "1.00"}
        ],
        "total": "5.00"
    }

    assert calculate_points(receipt) == 96


def test_rule4_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [{"shortDescription": f"Item {i}", "price": "0.01"} for i in range(99)],
        "total": "0.99"
    }

    assert calculate_points(receipt) == 264


# ----------------------------------------------------------------------------------------
# Rule 5 Tests: Points for Descriptions with Length Divisible by 3
# ----------------------------------------------------------------------------------------

def test_rule5_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Pop", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 85


def test_rule5_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Margherita Pizza", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule5_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "      Extraordinarily Delicious Organic Avocado Toast      ", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


# ----------------------------------------------------------------------------------------
# Rule 6 Tests: 6 Points if Purchase Day is Odd
# ----------------------------------------------------------------------------------------

def test_rule6_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule6_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-31",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule6_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-20",
        "purchaseTime": "12:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 78


# ----------------------------------------------------------------------------------------
# Rule 7 Tests: 10 Points if Purchase Time is Between 2:00PM and 4:00PM
# ----------------------------------------------------------------------------------------

def test_rule7_easy():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "14:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule7_medium():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "16:00",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84


def test_rule7_hard():
    receipt = {
        "retailer": "CVS",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:59",
        "items": [
            {"shortDescription": "Item", "price": "1.00"}
        ],
        "total": "1.00"
    }

    assert calculate_points(receipt) == 84
