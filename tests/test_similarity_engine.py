from src.similarity.engine import get_top_similar_products


def test_top_similar_products_returns_requested_count(monkeypatch):
    products = {
        "A": {
            "brand": "Brand A",
            "product_name": "Product A",
            "product_form": "cream",
        },
        "B": {
            "brand": "Brand B",
            "product_name": "Product B",
            "product_form": "cream",
        },
        "C": {
            "brand": "Brand C",
            "product_name": "Product C",
            "product_form": "lotion",
        },
    }

    pairs = [
        {
            "product_a_id": "A",
            "product_b_id": "B",
            "formula_similarity": 0.8,
            "ingredient_similarity": 0.7,
            "function_similarity": 0.9,
        },
        {
            "product_a_id": "A",
            "product_b_id": "C",
            "formula_similarity": 0.4,
            "ingredient_similarity": 0.3,
            "function_similarity": 0.8,
        },
        {
            "product_a_id": "B",
            "product_b_id": "C",
            "formula_similarity": 0.2,
            "ingredient_similarity": 0.1,
            "function_similarity": 0.7,
        },
    ]

    monkeypatch.setattr(
        "src.similarity.engine.compute_all_pairs",
        lambda _: pairs,
    )

    results = get_top_similar_products(
        products,
        "A",
        top_k=2,
    )

    assert len(results) == 2
    assert results[0]["product_id"] == "B"
    assert results[1]["product_id"] == "C"


def test_top_similar_products_orders_by_formula_similarity(
    monkeypatch,
):
    products = {
        "A": {
            "brand": "Brand A",
            "product_name": "Product A",
            "product_form": "cream",
        },
        "B": {
            "brand": "Brand B",
            "product_name": "Product B",
            "product_form": "cream",
        },
        "C": {
            "brand": "Brand C",
            "product_name": "Product C",
            "product_form": "lotion",
        },
    }

    pairs = [
        {
            "product_a_id": "A",
            "product_b_id": "B",
            "formula_similarity": 0.3,
            "ingredient_similarity": 0.9,
            "function_similarity": 0.9,
        },
        {
            "product_a_id": "A",
            "product_b_id": "C",
            "formula_similarity": 0.6,
            "ingredient_similarity": 0.2,
            "function_similarity": 0.5,
        },
    ]

    monkeypatch.setattr(
        "src.similarity.engine.compute_all_pairs",
        lambda _: pairs,
    )

    results = get_top_similar_products(
        products,
        "A",
        top_k=2,
    )

    assert results[0]["product_id"] == "C"
    assert results[1]["product_id"] == "B"