from tests.conftest import future_date, register_and_login


def _sample_prediction_payload(**overrides):
    payload = {
        "domain": "climate_environment",
        "hypothesis": "Global average surface temperature will exceed 1.5C above baseline in 2027.",
        "resolution_criteria": "Per the WMO annual state-of-the-climate report for 2027.",
        "resolution_date": future_date(days=180),
        "probability_estimate": 42.0,
        "rationale": "Based on current warming trajectory and ENSO forecasts.",
    }
    payload.update(overrides)
    return payload


def test_create_prediction_requires_auth(client):
    response = client.post("/predictions", json=_sample_prediction_payload())
    assert response.status_code == 401


def test_create_prediction_success(client):
    headers = register_and_login(client, "creator1")
    response = client.post("/predictions", json=_sample_prediction_payload(), headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "open"
    assert body["domain"] == "climate_environment"
    assert body["creator"]["username"] == "creator1"


def test_create_prediction_rejects_past_resolution_date(client):
    headers = register_and_login(client, "creator2")
    payload = _sample_prediction_payload(resolution_date="2020-01-01T00:00:00Z")
    response = client.post("/predictions", json=payload, headers=headers)
    assert response.status_code == 422


def test_create_prediction_rejects_out_of_range_probability(client):
    headers = register_and_login(client, "creator3")
    payload = _sample_prediction_payload(probability_estimate=142.0)
    response = client.post("/predictions", json=payload, headers=headers)
    assert response.status_code == 422


def test_list_predictions_filters_by_domain(client):
    headers = register_and_login(client, "creator4")
    client.post("/predictions", json=_sample_prediction_payload(domain="climate_environment"), headers=headers)
    client.post("/predictions", json=_sample_prediction_payload(domain="public_health"), headers=headers)

    response = client.get("/predictions", params={"domain": "public_health"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["domain"] == "public_health"


def test_get_prediction_includes_consensus_fields(client):
    headers = register_and_login(client, "creator5")
    created = client.post("/predictions", json=_sample_prediction_payload(), headers=headers).json()

    response = client.get(f"/predictions/{created['id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["forecast_count"] == 0
    assert body["crowd_consensus_probability"] is None


def test_get_nonexistent_prediction_returns_404(client):
    response = client.get("/predictions/does-not-exist")
    assert response.status_code == 404
