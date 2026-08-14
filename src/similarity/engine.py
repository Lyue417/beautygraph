from itertools import combinations

from sqlalchemy import text

from src.db import ENGINE
from src.similarity.metrics import (
    build_function_profile,
    cosine_similarity,
    jaccard_similarity,
    weighted_jaccard_similarity,
)


def load_similarity_inputs() -> dict[str, dict]:
    with ENGINE.connect() as conn:
        product_rows = conn.execute(
            text(
                """
                SELECT
                    product_id,
                    brand_raw,
                    product_name_raw,
                    product_form
                FROM raw.products_raw
                ORDER BY product_id
                """
            )
        ).mappings().all()

        ingredient_rows = conn.execute(
            text(
                """
                SELECT
                    product_id,
                    ingredient_id,
                    ingredient_position
                FROM normalized.product_ingredients
                ORDER BY product_id, ingredient_position
                """
            )
        ).mappings().all()

        function_rows = conn.execute(
            text(
                """
                SELECT
                    inf.ingredient_id,
                    f.function_name
                FROM normalized.ingredient_functions inf
                JOIN normalized.functions f
                    ON inf.function_id = f.function_id
                """
            )
        ).mappings().all()

    ingredient_functions: dict[int, set[str]] = {}

    for row in function_rows:
        ingredient_functions.setdefault(
            row["ingredient_id"],
            set(),
        ).add(row["function_name"])

    products = {
        row["product_id"]: {
            "product_id": row["product_id"],
            "brand": row["brand_raw"],
            "product_name": row["product_name_raw"],
            "product_form": row["product_form"],
            "positions": {},
        }
        for row in product_rows
    }

    for row in ingredient_rows:
        product_id = row["product_id"]
        ingredient_id = row["ingredient_id"]

        positions = products[product_id]["positions"]

        if ingredient_id in positions:
            raise ValueError(
                f"Duplicate normalized ingredient found: "
                f"{product_id}, ingredient_id={ingredient_id}"
            )

        positions[ingredient_id] = row["ingredient_position"]

    for product in products.values():
        positions = product["positions"]

        product["ingredient_set"] = set(positions)

        product["function_profile"] = build_function_profile(
            positions,
            ingredient_functions,
        )

    return products


def compute_pair_components(
    product_a: dict,
    product_b: dict,
) -> dict[str, float]:
    ingredient_similarity = jaccard_similarity(
        product_a["ingredient_set"],
        product_b["ingredient_set"],
    )

    formula_similarity = weighted_jaccard_similarity(
        product_a["positions"],
        product_b["positions"],
    )

    function_similarity = cosine_similarity(
        product_a["function_profile"],
        product_b["function_profile"],
    )

    return {
        "ingredient_similarity": ingredient_similarity,
        "formula_similarity": formula_similarity,
        "function_similarity": function_similarity,
    }


def compute_all_pairs(
    products: dict[str, dict],
) -> list[dict]:
    results = []

    for product_a_id, product_b_id in combinations(
        sorted(products),
        2,
    ):
        product_a = products[product_a_id]
        product_b = products[product_b_id]

        scores = compute_pair_components(
            product_a,
            product_b,
        )

        results.append(
            {
                "product_a_id": product_a_id,
                "product_b_id": product_b_id,
                **scores,
            }
        )

    return results


def get_top_similar_products(
    products: dict[str, dict],
    product_id: str,
    top_k: int = 5,
) -> list[dict]:
    pairs = compute_all_pairs(products)

    candidates = []

    for row in pairs:
        if row["product_a_id"] == product_id:
            other_id = row["product_b_id"]

        elif row["product_b_id"] == product_id:
            other_id = row["product_a_id"]

        else:
            continue

        other = products[other_id]

        candidates.append(
            {
                "product_id": other_id,
                "brand": other["brand"],
                "product_name": other["product_name"],
                "product_form": other["product_form"],
                "formula_similarity": row["formula_similarity"],
                "ingredient_similarity": row["ingredient_similarity"],
                "function_similarity": row["function_similarity"],
            }
        )

    candidates.sort(
        key=lambda row: row["formula_similarity"],
        reverse=True,
    )

    return candidates[:top_k]