# Daxita Backend — Financial Transaction Analyzer

A FastAPI microservice that accepts a list of financial transactions, computes a financial summary, evaluates risk flags, and returns a readiness classification. Built as part of the Daxita Backend Engineering Challenge.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI 0.135 |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Containerization | Docker |

---

## Project Structure

```
daxita-backend/
├── main.py           # FastAPI app and route definitions
├── models.py         # Pydantic request/response models
├── analyzer.py       # Core transaction analysis logic
├── requirements.txt  # Pinned Python dependencies
└── Dockerfile        # Container build instructions
```

---

## Getting Started

### Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

API is now live at `http://localhost:8000`

### Run with Docker

```bash
# Build image
docker build -t daxita-backend .

# Start container
docker run -d --name daxita-backend-app -p 8000:8000 daxita-backend
```

---

## API Reference

### `GET /`
Health check endpoint.

**Response**
```json
{
  "status": "ok",
  "service": "Daxita Financial Transaction Analyzer"
}
```

---

### `POST /analyse-file`
Accepts a list of transactions and returns a full financial summary with risk assessment.

**Request body**
```json
{
  "transactions": [
    { "id": "t1", "amount": 5000, "description": "Salary" },
    { "id": "t2", "amount": -200, "description": "Groceries" },
    { "id": "t3", "amount": -3000, "description": "Rent" },
    { "id": "t4", "amount": -2000, "description": "Car Loan" }
  ]
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique identifier for the transaction |
| `amount` | float | yes | Positive = inflow, negative = outflow |
| `description` | string | no | Human-readable label |

**Response**
```json
{
  "total_inflow": 5000.0,
  "total_outflow": -5200.0,
  "net_cash_flow": -200.0,
  "inflow_count": 1,
  "outflow_count": 3,
  "largest_inflow": 5000.0,
  "largest_outflow": -3000.0,
  "average_transaction_value": 2550.0,
  "risk_flags": [
    {
      "code": "NEGATIVE_NET_CASH_FLOW",
      "message": "Outflows exceed inflows -- Net cash flow is negative"
    },
    {
      "code": "LARGE_SINGLE_OUTFLOW",
      "message": "A single outflow exceeds 50% of total inflow"
    },
    {
      "code": "NSF_RISK",
      "message": "Potential insufficent detected based on funds available - Outflow exceeds running balance"
    }
  ],
  "readiness": "requires_clarification"
}
```

---

## Risk Flags

The analyzer applies four rules to detect financial risk:

| Code | Trigger Condition |
|---|---|
| `NEGATIVE_NET_CASH_FLOW` | Total outflows exceed total inflows (net cash flow < 0) |
| `LARGE_SINGLE_OUTFLOW` | A single outflow is greater than 50% of total inflows |
| `NSF_RISK` | Running balance dips below zero at any point in the transaction sequence |
| `LOW_INFLOW_FREQUENCY` | Fewer than 20% of all transactions are inflows |

---

## Readiness Classification

Based on the number of risk flags detected:

| Result | Condition |
|---|---|
| `strong` | Zero flags and positive net cash flow |
| `structured` | One or fewer flags |
| `requires_clarification` | Two or more flags |

---

## Interactive Docs

FastAPI auto-generates interactive documentation when the server is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Example cURL

**PowerShell**
```powershell
curl.exe --% -s -X POST http://localhost:8000/analyse-file `
  -H "Content-Type: application/json" `
  -d "{\"transactions\":[{\"id\":\"t1\",\"amount\":5000,\"description\":\"Salary\"},{\"id\":\"t2\",\"amount\":-200,\"description\":\"Groceries\"},{\"id\":\"t3\",\"amount\":-3000,\"description\":\"Rent\"},{\"id\":\"t4\",\"amount\":-2000,\"description\":\"Car Loan\"}]}"
```

**Linux / macOS**
```bash
curl -s -X POST http://localhost:8000/analyse-file \
  -H "Content-Type: application/json" \
  -d '{"transactions":[{"id":"t1","amount":5000,"description":"Salary"},{"id":"t2","amount":-200,"description":"Groceries"},{"id":"t3","amount":-3000,"description":"Rent"},{"id":"t4","amount":-2000,"description":"Car Loan"}]}'
```

---

## Docker Commands Reference

```bash
# Build
docker build -t daxita-backend .

# Run (detached)
docker run -d --name daxita-backend-app -p 8000:8000 daxita-backend

# View logs
docker logs -f daxita-backend-app

# Stop
docker stop daxita-backend-app

# Remove
docker rm daxita-backend-app
```
