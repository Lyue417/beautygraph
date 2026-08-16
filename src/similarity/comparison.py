from src.similarity.engine import compute_pair_components


FUNCTION_LABELS = {
    "barrier_supporting": "barrier-supporting",
    "texture_viscosity": "texture/viscosity",
    "fragrance_related": "fragrance-related",
    "active_treatment": "active-treatment",
}


def function_label(function_name: str) -> str:
    return FUNCTION_LABELS.get(
        function_name,
        function_name,
    )


def format_items(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return (
        ", ".join(items[:-1])
        + f", and {items[-1]}"
    )


def compare_ingredients(
    product_a: dict,
    product_b: dict,
) -> dict:
    positions_a = product_a["positions"]
    positions_b = product_b["positions"]

    shared_ids = positions_a.keys() & positions_b.keys()
    only_a_ids = positions_a.keys() - positions_b.keys()
    only_b_ids = positions_b.keys() - positions_a.keys()

    shared = [
        {
            "ingredient_id": ingredient_id,
            "name": product_a["ingredient_names"][ingredient_id],
            "position_a": positions_a[ingredient_id],
            "position_b": positions_b[ingredient_id],
        }
        for ingredient_id in shared_ids
    ]

    shared.sort(
        key=lambda row: (
            max(
                row["position_a"],
                row["position_b"],
            ),
            row["name"],
        )
    )

    shared_high_position = [
        row
        for row in shared
        if row["position_a"] <= 10
        and row["position_b"] <= 10
    ]

    only_a = [
        {
            "ingredient_id": ingredient_id,
            "name": product_a["ingredient_names"][ingredient_id],
            "position": positions_a[ingredient_id],
        }
        for ingredient_id in only_a_ids
    ]

    only_b = [
        {
            "ingredient_id": ingredient_id,
            "name": product_b["ingredient_names"][ingredient_id],
            "position": positions_b[ingredient_id],
        }
        for ingredient_id in only_b_ids
    ]

    only_a.sort(
        key=lambda row: (
            row["position"],
            row["name"],
        )
    )

    only_b.sort(
        key=lambda row: (
            row["position"],
            row["name"],
        )
    )

    return {
        "shared": shared,
        "shared_high_position": shared_high_position,
        "only_a": only_a,
        "only_b": only_b,
    }


def compare_functions(
    product_a: dict,
    product_b: dict,
) -> dict:
    profile_a = product_a["formula_profile"]
    profile_b = product_b["formula_profile"]

    shared = []

    for function_name in profile_a:
        share_a = profile_a[function_name]
        share_b = profile_b[function_name]

        if share_a > 0 and share_b > 0:
            shared.append(
                {
                    "function_name": function_name,
                    "share_a": share_a,
                    "share_b": share_b,
                    "shared_strength": min(
                        share_a,
                        share_b,
                    ),
                }
            )

    shared.sort(
        key=lambda row: (
            -row["shared_strength"],
            row["function_name"],
        )
    )

    differences = [
        {
            "function_name": function_name,
            "share_a": profile_a[function_name],
            "share_b": profile_b[function_name],
            "difference": (
                profile_a[function_name]
                - profile_b[function_name]
            ),
            "absolute_difference": abs(
                profile_a[function_name]
                - profile_b[function_name]
            ),
        }
        for function_name in profile_a
    ]

    differences.sort(
        key=lambda row: (
            -row["absolute_difference"],
            row["function_name"],
        )
    )

    return {
        "shared": shared,
        "differences": differences,
    }


def describe_function_difference(
    row: dict,
    product_a: dict,
    product_b: dict,
) -> str:
    function_name = function_label(
        row["function_name"]
    )

    share_a = row["share_a"]
    share_b = row["share_b"]

    if share_a == 0 and share_b > 0:
        return (
            f"{product_b['product_name']} has mapped signal "
            f"in the {function_name} group that is not present "
            f"in {product_a['product_name']}'s mapped profile "
            f"({share_b:.1%} vs {share_a:.1%})"
        )

    if share_b == 0 and share_a > 0:
        return (
            f"{product_a['product_name']} has mapped signal "
            f"in the {function_name} group that is not present "
            f"in {product_b['product_name']}'s mapped profile "
            f"({share_a:.1%} vs {share_b:.1%})"
        )

    if share_a > share_b:
        return (
            f"{product_a['product_name']} has a higher share "
            f"of the {function_name} group in the mapped profile "
            f"({share_a:.1%} vs {share_b:.1%})"
        )

    return (
        f"{product_b['product_name']} has a higher share "
        f"of the {function_name} group in the mapped profile "
        f"({share_b:.1%} vs {share_a:.1%})"
    )


def build_explanation(
    product_a: dict,
    product_b: dict,
    ingredient_comparison: dict,
    function_comparison: dict,
) -> str:
    sentences = []

    shared = ingredient_comparison["shared"]
    shared_high = ingredient_comparison[
        "shared_high_position"
    ]

    if shared_high:
        names = format_items(
            [
                row["name"]
                for row in shared_high[:5]
            ]
        )

        sentences.append(
            f"They share {len(shared)} normalized ingredients, "
            f"with high-position overlap including {names}."
        )

    elif shared:
        sentences.append(
            f"They share {len(shared)} normalized ingredients, "
            "but none are within the top 10 positions "
            "of both products."
        )

    else:
        sentences.append(
            "They do not share any normalized ingredients."
        )

    unique_high_a = [
        row
        for row in ingredient_comparison["only_a"]
        if row["position"] <= 10
    ]

    unique_high_b = [
        row
        for row in ingredient_comparison["only_b"]
        if row["position"] <= 10
    ]

    unique_parts = []

    if unique_high_a:
        names = format_items(
            [
                row["name"]
                for row in unique_high_a[:3]
            ]
        )

        unique_parts.append(
            f"{names} in {product_a['product_name']}"
        )

    if unique_high_b:
        names = format_items(
            [
                row["name"]
                for row in unique_high_b[:3]
            ]
        )

        unique_parts.append(
            f"{names} in {product_b['product_name']}"
        )

    if unique_parts:
        sentences.append(
            "High-position ingredients unique to one product include "
            + "; ".join(unique_parts)
            + "."
        )

    shared_functions = function_comparison["shared"][:3]

    if len(shared_functions) == 1:
        label = function_label(
            shared_functions[0]["function_name"]
        )

        sentences.append(
            "The strongest shared mapped function group is "
            f"{label}."
        )

    elif shared_functions:
        labels = format_items(
            [
                function_label(row["function_name"])
                for row in shared_functions
            ]
        )

        sentences.append(
            "Both products show their strongest shared mapped "
            f"signals in the {labels} groups."
        )

    differences = [
        row
        for row in function_comparison["differences"]
        if abs(
            row["share_a"] - row["share_b"]
        ) > 1e-12
    ][:2]

    if differences:
        difference_text = [
            describe_function_difference(
                row,
                product_a,
                product_b,
            )
            for row in differences
        ]

        if len(difference_text) == 1:
            sentences.append(
                "The largest mapped function-profile difference is: "
                + difference_text[0]
                + "."
            )

        else:
            sentences.append(
                "The largest mapped function-profile differences are: "
                + "; ".join(difference_text)
                + "."
            )

    else:
        sentences.append(
            "The two mapped function profiles have the same "
            "distribution across the current function groups."
        )

    sentences.append(
        "This function comparison is based on mapped ingredient "
        f"coverage of {product_a['function_mapping_coverage']:.1%} "
        f"for {product_a['product_name']} and "
        f"{product_b['function_mapping_coverage']:.1%} "
        f"for {product_b['product_name']}."
    )

    return " ".join(sentences)


def build_product_comparison(
    products: dict[str, dict],
    product_a_id: str,
    product_b_id: str,
) -> dict:
    product_a = products[product_a_id]
    product_b = products[product_b_id]

    similarity = compute_pair_components(
        product_a,
        product_b,
    )

    ingredient_comparison = compare_ingredients(
        product_a,
        product_b,
    )

    function_comparison = compare_functions(
        product_a,
        product_b,
    )

    explanation = build_explanation(
        product_a,
        product_b,
        ingredient_comparison,
        function_comparison,
    )

    return {
        "product_a": {
            "product_id": product_a["product_id"],
            "brand": product_a["brand"],
            "product_name": product_a["product_name"],
            "product_form": product_a["product_form"],
            "formula_profile": product_a["formula_profile"],
            "function_mapping_coverage": product_a[
                "function_mapping_coverage"
            ],
        },
        "product_b": {
            "product_id": product_b["product_id"],
            "brand": product_b["brand"],
            "product_name": product_b["product_name"],
            "product_form": product_b["product_form"],
            "formula_profile": product_b["formula_profile"],
            "function_mapping_coverage": product_b[
                "function_mapping_coverage"
            ],
        },
        "similarity": similarity,
        "ingredients": ingredient_comparison,
        "functions": function_comparison,
        "explanation": explanation,
    }