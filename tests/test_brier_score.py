import pytest

from app.services.brier import calculate_brier_score, mean_brier_score


def test_perfect_confident_correct_forecast_scores_zero():
    assert calculate_brier_score(100.0, True) == 0.0


def test_perfect_confident_wrong_forecast_scores_one():
    assert calculate_brier_score(100.0, False) == 1.0


def test_coin_flip_forecast_scores_quarter_point_two_five():
    assert calculate_brier_score(50.0, True) == 0.25
    assert calculate_brier_score(50.0, False) == 0.25


def test_intermediate_forecast():
    # p=0.7, outcome=True -> (0.7 - 1)^2 = 0.09
    assert calculate_brier_score(70.0, True) == pytest.approx(0.09)
    # p=0.7, outcome=False -> (0.7 - 0)^2 = 0.49
    assert calculate_brier_score(70.0, False) == pytest.approx(0.49)


def test_rejects_out_of_range_probability():
    with pytest.raises(ValueError):
        calculate_brier_score(150.0, True)
    with pytest.raises(ValueError):
        calculate_brier_score(-10.0, True)


def test_mean_brier_score_of_empty_list_is_none():
    assert mean_brier_score([]) is None


def test_mean_brier_score_averages_correctly():
    assert mean_brier_score([0.0, 0.5, 1.0]) == pytest.approx(0.5)
