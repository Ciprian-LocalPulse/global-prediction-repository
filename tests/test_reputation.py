from app.core.enums import UserRole
from app.models.user import User
from tests.conftest import future_date, register_and_login


def _promote_to_oracle(db_session, username: str):
    user = db_session.query(User).filter(User.username == username).first()
    user.role = UserRole.ORACLE
    db_session.add(user)
    db_session.commit()


def _create_prediction(client, headers, probability_estimate=40.0):
    payload = {
        "domain": "public_health",
        "hypothesis": "A novel influenza strain will trigger a WHO PHEIC declaration within 18 months.",
        "resolution_criteria": "Formal WHO Public Health Emergency of International Concern declaration.",
        "resolution_date": future_date(days=30),
        "probability_estimate": probability_estimate,
        "rationale": "Based on current surveillance data from WHO FluNet.",
    }
    return client.post("/predictions", json=payload, headers=headers).json()


def test_non_oracle_cannot_resolve_prediction(client):
    creator_headers = register_and_login(client, "hcreator1")
    prediction = _create_prediction(client, creator_headers)

    response = client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": True},
        headers=creator_headers,
    )
    assert response.status_code == 403


def test_resolving_true_scores_forecasters_and_updates_reputation(client, db_session):
    creator_headers = register_and_login(client, "hcreator2")
    prediction = _create_prediction(client, creator_headers, probability_estimate=40.0)

    # Two forecasters take opposing positions.
    confident_headers = register_and_login(client, "confident_forecaster")
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 90.0},
        headers=confident_headers,
    )

    skeptical_headers = register_and_login(client, "skeptical_forecaster")
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 10.0},
        headers=skeptical_headers,
    )

    oracle_headers = register_and_login(client, "oracle_user")
    _promote_to_oracle(db_session, "oracle_user")

    resolve_response = client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": True},
        headers=oracle_headers,
    )
    assert resolve_response.status_code == 200
    body = resolve_response.json()
    assert body["status"] == "resolved_true"
    assert body["final_brier_score"] is not None

    confident_profile = client.get("/users/me", headers=confident_headers).json()
    skeptical_profile = client.get("/users/me", headers=skeptical_headers).json()

    # The confident forecaster (90% on a True outcome) should end up with
    # a much higher accuracy score than the skeptical one (10% on a True
    # outcome).
    assert confident_profile["global_accuracy_score"] > skeptical_profile["global_accuracy_score"]
    assert confident_profile["resolved_forecast_count"] == 1
    assert skeptical_profile["resolved_forecast_count"] == 1


def test_ambiguous_resolution_does_not_affect_reputation(client, db_session):
    creator_headers = register_and_login(client, "hcreator3")
    prediction = _create_prediction(client, creator_headers)

    forecaster_headers = register_and_login(client, "unaffected_forecaster")
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 65.0},
        headers=forecaster_headers,
    )

    oracle_headers = register_and_login(client, "oracle_user2")
    _promote_to_oracle(db_session, "oracle_user2")

    resolve_response = client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": True, "ambiguous": True},
        headers=oracle_headers,
    )
    assert resolve_response.status_code == 200
    assert resolve_response.json()["status"] == "ambiguous"

    profile = client.get("/users/me", headers=forecaster_headers).json()
    assert profile["global_accuracy_score"] == 50.0
    assert profile["resolved_forecast_count"] == 0


def test_cannot_resolve_already_resolved_prediction(client, db_session):
    creator_headers = register_and_login(client, "hcreator4")
    prediction = _create_prediction(client, creator_headers)

    oracle_headers = register_and_login(client, "oracle_user3")
    _promote_to_oracle(db_session, "oracle_user3")

    client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": False},
        headers=oracle_headers,
    )
    second_attempt = client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": True},
        headers=oracle_headers,
    )
    assert second_attempt.status_code == 409


def test_leaderboard_respects_min_resolved_threshold(client, db_session):
    creator_headers = register_and_login(client, "hcreator5")
    prediction = _create_prediction(client, creator_headers)

    forecaster_headers = register_and_login(client, "one_hit_wonder")
    client.post(
        f"/predictions/{prediction['id']}/forecasts",
        json={"probability_estimate": 80.0},
        headers=forecaster_headers,
    )

    oracle_headers = register_and_login(client, "oracle_user4")
    _promote_to_oracle(db_session, "oracle_user4")
    client.post(
        f"/oracle/predictions/{prediction['id']}/resolve",
        json={"outcome": True},
        headers=oracle_headers,
    )

    # Default min_resolved is 3; this forecaster only has 1 resolved forecast.
    default_leaderboard = client.get("/leaderboard").json()
    usernames = [u["username"] for u in default_leaderboard]
    assert "one_hit_wonder" not in usernames

    relaxed_leaderboard = client.get("/leaderboard", params={"min_resolved": 1}).json()
    usernames = [u["username"] for u in relaxed_leaderboard]
    assert "one_hit_wonder" in usernames
