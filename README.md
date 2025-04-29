# Receipt Processor

This is a Flask-based API that calculates reward points from receipts based on specific rules.

---

## Features

- Processes receipt data and returns a unique receipt ID
- Calculates reward points based on multiple rules
- Fully tested with 20+ unit tests
- Dockerized for easy setup and execution

---

## Requirements

- Docker
- Or: Python 3.11 and pip if running locally

---

## Running with Docker

### Build the Docker image

```bash
docker build -t fetch-receipts .
```

### Run the container (default port)

```bash
docker run -p 5000:5000 fetch-receipts
```

If port 5000 is unavailable, you can map to any local port:

```bash
docker run -p 5050:5000 fetch-receipts
```

Then access the API at: `http://localhost:5050` or whatever port you chose.

---

## Running Locally (Without Docker)

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## API Endpoints

### `POST /receipts/process`

Submit a receipt JSON object and get back a receipt ID.

**Request:**
```json
{
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
```

**Response:**
```json
{ "id": "a-uuid-value" }
```

---

### `GET /receipts/<id>/points`

Returns the calculated points for the specified receipt ID.

**Response:**
```json
{ "points": 28 }
```

---

## Running Tests

```bash
PYTHONPATH=. pytest
```

Test cases are located in `tests/` and cover:
- API
- All 7 rule conditions
- Easy, medium, hard test cases
- Edge case handling

---

## Project Structure

```
fetch-receipts/
├── app.py
├── routes/
├── services/
├── storage/
├── tests/
├── requirements.txt
└── Dockerfile
```

---

## Author

Sebastian Krzysiak
