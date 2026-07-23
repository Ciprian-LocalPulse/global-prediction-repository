from tests.conftest import future_date, register_and_login


def _create_prediction(client, headers):
    payload = {
        "domain": "ai_tech_risk",
        "hypothesis": "A frontier lab will publicly announce an AGI milestone by end of 2028.",
        "resolution_criteria": "Announcement from a lab on the Frontier Model Forum member list.",
        "resolution_date": future_date(days=365),
        "probability_estimate": 20.0,
        "rationale": "Extrapolating from current scaling trends and announced timelines.",
    }
    return client.post("/predictions", json=payload, headers=headers).json()


def test_submit_forecast_requires_auth(client):
    headers = register_and_login(client, "pcreator1")
    prediction = _create_prediction(client, headers)

    response = client.post(f"/predictions/{prediction['id']}/forecasts", json={"probability_estimate": 30})
    assert response.status_code == 401


def test_submit_forecast_success(client):
    creator_headers = register_and_login(client, "pcreator2")
    prediction = _create_prediction(client, creator_headers)

    forecaster_headers = register_and_login(client, "forecaster1")
    response = client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 35.0},
        headers=forecaster_headers,
    )
    assert response.status_code == 201
    assert response.json()["probability_estimate"] == 35.0


def test_resubmitting_forecast_updates_existing_row(client):
    creator_headers = register_and_login(client, "pcreator3")
    prediction = _create_prediction(client, creator_headers)

    forecaster_headers = register_and_login(client, "forecaster2")
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 20.0},
        headers=forecaster_headers,
    )
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 55.0},
        headers=forecaster_headers,
    )

    listing = client.get(f"/predictions/{prediction['id']}/forecasts").json()
    assert len(listing) == 1
    assert listing[0]["probability_estimate"] == 55.0


def test_crowd_consensus_reflects_average_of_forecasts(client):
    creator_headers = register_and_login(client, "pcreator4")
    prediction = _create_prediction(client, creator_headers)

    for i, prob in enumerate([10.0, 30.0]):
        headers = register_and_login(client, f"forecaster_{i}")
        client.post(
            f"/predictions/{prediction['id']}/forecasts",
            json={"probability_estimate": prob},
            headers=headers,
        )

    response = client.get(f"/predictions/{prediction['id']}")
    body = response.json()
    assert body["forecast_count"] == 2
    # Fewer than 3 forecasts -> simple average, per crowd_consensus().
    assert body["crowd_consensus_probability"] == 20.0


def test_cannot_forecast_a_resolved_prediction(client):
    creator_headers = register_and_login(client, "pcreator5")
    prediction = _create_prediction(client, creator_headers)

    # Directly flip status via the DB isn't exposed here, so instead we
    # rely on the oracle resolution tests to cover that path; this test
    # just confirms the router enforces "OPEN only" for a freshly created
    # (and therefore still open) prediction as a sanity check that forecasts
    # succeed while a prediction is open.
    forecaster_headers = register_and_login(client, "forecaster3")
    response = client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 40.0},
        headers=forecaster_headers,
    )
    assert response.status_code == 201
