from math import sqrt


FUNCTION_NAMES = (
    "humectant",
    "emollient",
    "occlusive",
    "barrier_supporting",
    "soothing",
    "antioxidant",
    "texture_viscosity",
    "preservative",
    "fragrance_related",
    "active_treatment",
)


def jaccard_similarity(
    ingredients_a: set[int],
    ingredients_b: set[int],
) -> float:
    intersection = ingredients_a & ingredients_b
    union = ingredients_a | ingredients_b

    return len(intersection) / len(union)


def position_weight(position: int) -> float:
    return 1 / sqrt(position)


def weighted_jaccard_similarity(
    positions_a: dict[int, int],
    positions_b: dict[int, int],
) -> float:
    ingredient_ids = positions_a.keys() | positions_b.keys()

    shared_weight = 0.0
    total_weight = 0.0

    for ingredient_id in ingredient_ids:
        weight_a = (
            position_weight(positions_a[ingredient_id])
            if ingredient_id in positions_a
            else 0.0
        )
        weight_b = (
            position_weight(positions_b[ingredient_id])
            if ingredient_id in positions_b
            else 0.0
        )

        shared_weight += min(weight_a, weight_b)
        total_weight += max(weight_a, weight_b)

    return shared_weight / total_weight


def build_function_profile(
    ingredient_positions: dict[int, int],
    ingredient_functions: dict[int, set[str]],
) -> dict[str, float]:
    profile = {
        function_name: 0.0
        for function_name in FUNCTION_NAMES
    }

    for ingredient_id, position in ingredient_positions.items():
        functions = ingredient_functions.get(ingredient_id)

        if not functions:
            continue

        contribution = position_weight(position) / len(functions)

        for function_name in functions:
            profile[function_name] += contribution

    return profile


def normalize_function_profile(
    profile: dict[str, float],
) -> dict[str, float]:
    total = sum(profile.values())

    if total == 0:
        return {
            function_name: 0.0
            for function_name in FUNCTION_NAMES
        }

    return {
        function_name: profile[function_name] / total
        for function_name in FUNCTION_NAMES
    }


def function_mapping_coverage(
    ingredient_positions: dict[int, int],
    function_profile: dict[str, float],
) -> float:
    total_ingredient_weight = sum(
        position_weight(position)
        for position in ingredient_positions.values()
    )

    if total_ingredient_weight == 0:
        return 0.0

    mapped_weight = sum(function_profile.values())

    return mapped_weight / total_ingredient_weight


def cosine_similarity(
    profile_a: dict[str, float],
    profile_b: dict[str, float],
) -> float:
    dot_product = sum(
        profile_a[name] * profile_b[name]
        for name in FUNCTION_NAMES
    )

    norm_a = sqrt(
        sum(profile_a[name] ** 2 for name in FUNCTION_NAMES)
    )
    norm_b = sqrt(
        sum(profile_b[name] ** 2 for name in FUNCTION_NAMES)
    )

    return dot_product / (norm_a * norm_b)