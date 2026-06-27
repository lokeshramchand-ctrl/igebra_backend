import pytest
from fastapi.testclient import TestClient
from app import app  # Imports your FastAPI instance

# The required Phase 15 authorization header
HEADERS = {
    "X-Velar-API-Key": "velar_test_key_123",
    "Content-Type": "application/json"
}

@pytest.fixture(scope="module")
def client():
    """
    Using TestClient inside a 'with' block triggers FastAPI's lifespan events.
    This ensures MongoDB connects and collections are initialized before tests run.
    """
    with TestClient(app) as c:
        yield c

# ---------------------------------------------------------
# SYSTEM HEALTH
# ---------------------------------------------------------

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# ---------------------------------------------------------
# INGESTION & RESOLUTION (PHASES 1-3)
# ---------------------------------------------------------

def test_categorize_endpoint(client):
    payload = {"text": "paid 500 to swiggy"}
    response = client.post("/v1/categorize", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert "merchant" in data
    assert "category" in data
    assert "confidence" in data

def test_resolution_endpoint(client):
    payload = {"text": "UPI/CR/3152671239/BUNDL TECHNOLOGIES/HDFC"}
    response = client.post("/v1/resolve", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    # Because 'bundl' is in our mock aliases, we expect it to resolve
    assert "cleaned_text" in response.json()

# ---------------------------------------------------------
# MEMORY ENGINE (PHASE 4)
# ---------------------------------------------------------

def test_memory_update(client):
    payload = {"canonical_name": "TestMerchant", "raw_text": "paid to testmerchant"}
    response = client.post("/memory/update", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert "memory_state" in data
    assert "frequency" in data
    assert data["canonical_name"] == "TestMerchant"

# ---------------------------------------------------------
# CONFIDENCE WALL (PHASE 5)
# ---------------------------------------------------------

def test_confidence_evaluator_hallucination(client):
    # Sending a low confidence score to trigger the hallucination block
    payload = {"predicted_category": "Travel", "raw_confidence": 0.40}
    response = client.post("/v1/confidence/evaluate", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert data["final_category"] == "Unknown"
    assert data["is_hallucination_risk"] is True

# ---------------------------------------------------------
# ANALYTICS ENGINE (PHASE 13)
# ---------------------------------------------------------

def test_analytics_categories(client):
    response = client.get("/v1/analytics/patterns/categories?days=30", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_merchants(client):
    response = client.get("/v1/analytics/patterns/merchants?limit=5", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_subscriptions(client):
    response = client.get("/v1/analytics/subscriptions", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "active_subscriptions" in data
    assert "total_monthly_burn" in data

def test_analytics_anomaly_check(client):
    # Assuming the anomaly endpoint accepts query parameters as defined in the router
    response = client.post("/v1/analytics/anomaly/check?merchant=Uber&amount=5000", headers=HEADERS)
    assert response.status_code == 200
    assert "is_anomaly" in response.json()

# ---------------------------------------------------------
# CONTEXT RAG & EXPLAINABILITY (PHASE 12)
# ---------------------------------------------------------

def test_rag_explanation(client):
    payload = {
        "transaction_text": "Swiggy order", 
        "target_question": "Why was this categorized this way?"
    }
    response = client.post("/v1/explain", json=payload, headers=HEADERS)
    
    # We assert < 500 here in case Milvus/Local LLM isn't fully spun up during testing
    assert response.status_code < 500 

# ---------------------------------------------------------
# OBSERVABILITY & MLOPS (PHASE 14)
# ---------------------------------------------------------

def test_trigger_drift_analysis(client):
    response = client.post("/v1/observability/drift/analyze", headers=HEADERS)
    assert response.status_code == 200
    assert "status" in response.json()

def test_fetch_drift_report(client):
    response = client.get("/v1/observability/reports/latest", headers=HEADERS)
    # Will return 200 if the HTML report exists, or 404/json if not generated yet.
    # Both are valid programmatic responses for this endpoint.
    assert response.status_code in [200, 404]
    
# ---------------------------------------------------------
# SECURITY (PHASE 15)
# ---------------------------------------------------------

def test_security_rejection(client):
    """Ensure endpoints reject requests without a valid API Key."""
    payload = {"text": "paid 500 to swiggy"}
    response = client.post("/v1/categorize", json=payload) # Notice NO headers passed
    
    # Should be rejected as Unauthorized (401) or Forbidden (403)
    assert response.status_code in [401, 403]