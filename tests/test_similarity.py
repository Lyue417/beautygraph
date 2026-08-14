from math import sqrt

import pytest

from src.similarity.metrics import (
    build_function_profile,
    cosine_similarity,
    jaccard_similarity,
    position_weight,
    weighted_jaccard_similarity,
)


def test_jaccard_similarity():
    ingredients_a = {1, 2, 3, 4}
    ingredients_b = {1, 2, 4, 5}

    assert jaccard_similarity(
        ingredients_a,
        ingredients_b,
    ) == pytest.approx(3 / 5)


def test_position_weight():
    assert position_weight(1) == pytest.approx(1.0)
    assert position_weight(4) == pytest.approx(0.5)
    assert position_weight(9) == pytest.approx(1 / 3)


def test_weighted_jaccard_rewards_similar_positions():
    positions_a = {
        1: 1,
        2: 2,
    }

    positions_b_close = {
        1: 1,
        2: 3,
    }

    positions_b_far = {
        1: 1,
        2: 20,
    }

    close_score = weighted_jaccard_similarity(
        positions_a,
        positions_b_close,
    )
    far_score = weighted_jaccard_similarity(
        positions_a,
        positions_b_far,
    )

    assert close_score > far_score


def test_function_profile_splits_multifunction_weight():
    positions = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
    }

    functions = {
        1: {"humectant"},
        2: {"humectant"},
        3: {"emollient", "occlusive"},
        4: {"humectant", "soothing"},
    }

    profile = build_function_profile(
        positions,
        functions,
    )

    assert profile["humectant"] == pytest.approx(
        1.0 + 1 / sqrt(2) + 0.25
    )
    assert profile["emollient"] == pytest.approx(
        1 / (2 * sqrt(3))
    )
    assert profile["occlusive"] == pytest.approx(
        1 / (2 * sqrt(3))
    )
    assert profile["soothing"] == pytest.approx(0.25)


def test_cosine_similarity_is_one_for_same_profile_shape():
    profile_a = {
        "humectant": 2.0,
        "emollient": 1.0,
        "occlusive": 0.0,
        "barrier_supporting": 0.0,
        "soothing": 0.0,
        "antioxidant": 0.0,
        "texture_viscosity": 0.0,
        "preservative": 0.0,
        "fragrance_related": 0.0,
        "active_treatment": 0.0,
    }

    profile_b = {
        name: value * 2
        for name, value in profile_a.items()
    }

    assert cosine_similarity(
        profile_a,
        profile_b,
    ) == pytest.approx(1.0)