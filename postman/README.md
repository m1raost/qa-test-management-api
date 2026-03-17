# Postman Collection

## Import

1. Open Postman
2. Click **Import** → select `qa-api.postman_collection.json`
3. The collection appears with all requests grouped by resource

## Setup

The collection uses two variables — set them under **Collection → Variables**:

| Variable | Default | Description |
|---|---|---|
| `base_url` | `http://localhost:8000` | Change if running on a different port |
| `token` | _(empty)_ | Filled automatically after login |

## Running the collection

1. Start the API: `uvicorn main:app --reload`
2. Run **Auth / Register** to create your account
3. Run **Auth / Login** — the token is saved automatically
4. Run any other request — the `Bearer {{token}}` header is pre-filled

## Request order (for a full flow)

```
Auth/Register
Auth/Login          ← saves token
Test Suites/Create  ← note the id returned
Test Cases/Create   ← use that suite id
Test Runs/Create
Test Results/Record ← use the run id and case id
```
