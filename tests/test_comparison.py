import pytest

from src.similarity.comparison import (
    build_explanation,
    build_product_comparison,
    compare_functions,
    compare_ingredients,
)


def test_compare_ingredients():
    product_a = {
        "positions": {
            1: 1,
            2: 4,
            3: 12,
        },
        "ingredient_names": {
            1: "water",
            2: "glycerin",
            3: "niacinamide",
        },
    }

    product_b = {
        "positions": {
            1: 1,
            2: 6,
            4: 3,
        },
        "ingredient_names": {
            1: "water",
            2: "glycerin",
            4: "dimethicone",
        },
    }

    result = compare_ingredients(
        product_a,
        product_b,
    )

    assert [
        row["name"]
        for row in result["shared"]
    ] == [
        "water",
        "glycerin",
    ]

    assert [
        row["name"]
        for row in result["shared_high_position"]
    ] == [
        "water",
        "glycerin",
    ]

    assert result["only_a"][0]["name"] == "niacinamide"
    assert result["only_b"][0]["name"] == "dimethicone"


def test_shared_high_position_requires_both_products():
    product_a = {
        "positions": {
            1: 2,
        },
        "ingredient_names": {
            1: "glycerin",
        },
    }

    product_b = {
        "positions": {
            1: 20,
        },
        "ingredient_names": {
            1: "glycerin",
        },
    }

    result = compare_ingredients(
        product_a,
        product_b,
    )

    assert len(result["shared"]) == 1
    assert result["shared_high_position"] == []


def test_compare_functions_orders_shared_strength():
    product_a = {
        "formula_profile": {
            "humectant": 0.40,
            "emollient": 0.30,
            "occlusive": 0.30,
        }
    }

    product_b = {
        "formula_profile": {
            "humectant": 0.35,
            "emollient": 0.05,
            "occlusive": 0.60,
        }
    }

    result = compare_functions(
        product_a,
        product_b,
    )

    assert result["shared"][0]["function_name"] == "humectant"
    assert result["shared"][0]["shared_strength"] == pytest.approx(
        0.35
    )


def test_compare_functions_orders_largest_difference():
    product_a = {
        "formula_profile": {
            "humectant": 0.40,
            "emollient": 0.30,
            "occlusive": 0.30,
        }
    }

    product_b = {
        "formula_profile": {
            "humectant": 0.35,
            "emollient": 0.05,
            "occlusive": 0.60,
        }
    }

    result = compare_functions(
        product_a,
        product_b,
    )

    assert (
        result["differences"][0]["function_name"]
        == "occlusive"
    )

    assert result["differences"][0][
        "absolute_difference"
    ] == pytest.approx(0.30)


def test_build_explanation_is_deterministic():
    product_a = {
        "product_name": "Product A",
        "function_mapping_coverage": 0.8,
    }

    product_b = {
        "product_name": "Product B",
        "function_mapping_coverage": 0.7,
    }

    ingredients = {
        "shared": [
            {
                "name": "water",
            },
            {
                "name": "glycerin",
            },
        ],
        "shared_high_position": [
            {
                "name": "water",
            },
            {
                "name": "glycerin",
            },
        ],
        "only_a": [
            {
                "name": "petrolatum",
                "position": 5,
            }
        ],
        "only_b": [
            {
                "name": "niacinamide",
                "position": 4,
            }
        ],
    }

    functions = {
        "shared": [
            {
                "function_name": "humectant",
                "share_a": 0.3,
                "share_b": 0.35,
            }
        ],
        "differences": [
            {
                "function_name": "barrier_supporting",
                "share_a": 0.2,
                "share_b": 0.3,
            }
        ],
    }

    first = build_explanation(
        product_a,
        product_b,
        ingredients,
        functions,
    )

    second = build_explanation(
        product_a,
        product_b,
        ingredients,
        functions,
    )

    assert first == second
    assert "water" in first
    assert "glycerin" in first
    assert "petrolatum" in first
    assert "niacinamide" in first
    assert "barrier-supporting" in first


def test_build_product_comparison():
    products = {
        "A": {
            "product_id": "A",
            "brand": "Brand A",
            "product_name": "Product A",
            "product_form": "cream",
            "positions": {
                1: 1,
                2: 2,
            },
            "ingredient_names": {
                1: "water",
                2: "glycerin",
            },
            "ingredient_set": {
                1,
                2,
            },
            "function_profile": {
                "humectant": 1.0,
                "emollient": 0.0,
                "occlusive": 0.0,
                "barrier_supporting": 0.0,
                "soothing": 0.0,
                "antioxidant": 0.0,
                "texture_viscosity": 0.0,
                "preservative": 0.0,
                "fragrance_related": 0.0,
                "active_treatment": 0.0,
            },
            "formula_profile": {
                "humectant": 1.0,
                "emollient": 0.0,
                "occlusive": 0.0,
                "barrier_supporting": 0.0,
                "soothing": 0.0,
                "antioxidant": 0.0,
                "texture_viscosity": 0.0,
                "preservative": 0.0,
                "fragrance_related": 0.0,
                "active_treatment": 0.0,
            },
            "function_mapping_coverage": 1.0,
        },
        "B": {
            "product_id": "B",
            "brand": "Brand B",
            "product_name": "Product B",
            "product_form": "lotion",
            "positions": {
                1: 1,
                2: 3,
            },
            "ingredient_names": {
                1: "water",
                2: "glycerin",
            },
            "ingredient_set": {
                1,
                2,
            },
            "function_profile": {
                "humectant": 1.0,
                "emollient": 0.0,
                "occlusive": 0.0,
                "barrier_supporting": 0.0,
                "soothing": 0.0,
                "antioxidant": 0.0,
                "texture_viscosity": 0.0,
                "preservative": 0.0,
                "fragrance_related": 0.0,
                "active_treatment": 0.0,
            },
            "formula_profile": {
                "humectant": 1.0,
                "emollient": 0.0,
                "occlusive": 0.0,
                "barrier_supporting": 0.0,
                "soothing": 0.0,
                "antioxidant": 0.0,
                "texture_viscosity": 0.0,
                "preservative": 0.0,
                "fragrance_related": 0.0,
                "active_treatment": 0.0,
            },
            "function_mapping_coverage": 1.0,
        },
    }

    result = build_product_comparison(
        products,
        "A",
        "B",
    )

    assert result["product_a"]["product_id"] == "A"
    assert result["product_b"]["product_id"] == "B"

    assert result["similarity"][
        "ingredient_similarity"
    ] == pytest.approx(1.0)

    assert "ingredients" in result
    assert "functions" in result
    assert "explanation" in result


def test_explanation_handles_no_shared_ingredients():
    product_a = {
        "product_name": "Product A",
        "function_mapping_coverage": 0.8,
    }

    product_b = {
        "product_name": "Product B",
        "function_mapping_coverage": 0.8,
    }

    ingredients = {
        "shared": [],
        "shared_high_position": [],
        "only_a": [],
        "only_b": [],
    }

    functions = {
        "shared": [],
        "differences": [],
    }

    explanation = build_explanation(
        product_a,
        product_b,
        ingredients,
        functions,
    )

    assert (
        "They do not share any normalized ingredients."
        in explanation
    )


def test_explanation_does_not_create_false_difference():
    product_a = {
        "product_name": "Product A",
        "function_mapping_coverage": 1.0,
    }

    product_b = {
        "product_name": "Product B",
        "function_mapping_coverage": 1.0,
    }

    ingredients = {
        "shared": [],
        "shared_high_position": [],
        "only_a": [],
        "only_b": [],
    }

    functions = {
        "shared": [
            {
                "function_name": "humectant",
                "share_a": 1.0,
                "share_b": 1.0,
            }
        ],
        "differences": [
            {
                "function_name": "humectant",
                "share_a": 1.0,
                "share_b": 1.0,
            }
        ],
    }

    explanation = build_explanation(
        product_a,
        product_b,
        ingredients,
        functions,
    )

    assert "has a higher share" not in explanation
    assert "same distribution" in explanation