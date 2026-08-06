from src.normalization.normalize_ingredients import normalize_ingredient


def test_case_and_whitespace_normalization():
    assert normalize_ingredient("  GLYCERIN  ") == (
        "glycerin",
        "case_whitespace",
    )


def test_internal_whitespace_normalization():
    assert normalize_ingredient("SODIUM   HYALURONATE") == (
        "sodium hyaluronate",
        "case_whitespace",
    )


def test_water_aliases():
    variants = [
        "Water",
        "Aqua",
        "Aqua (Water)",
        "AQUA / WATER / EAU",
        "AQUA/WATER/EAU",
        "Water/Aqua/Eau",
        "Aqua/water/eau",
        "AQUA / WATER",
        "Water (Aqua)",
        "Water\\Aqua\\Eau",
    ]

    for variant in variants:
        assert normalize_ingredient(variant) == (
            "water",
            "alias",
        )


def test_fragrance_aliases():
    variants = [
        "Fragrance (Parfum)",
        "PARFUM / FRAGRANCE",
        "PARFUM/FRAGRANCE",
        "Parfum/fragrance",
    ]

    for variant in variants:
        assert normalize_ingredient(variant) == (
            "fragrance",
            "alias",
        )


def test_slash_compound_is_not_generally_split():
    assert normalize_ingredient(
        "Caprylic/Capric Triglyceride"
    ) == (
        "caprylic/capric triglyceride",
        "case_whitespace",
    )


def test_numeric_comma_is_preserved():
    assert normalize_ingredient("1,2-Hexanediol") == (
        "1,2-hexanediol",
        "case_whitespace",
    )


def test_disodium_edta_broken_hyphen_alias():
    assert normalize_ingredient("Diso- Dium Edta") == (
        "disodium edta",
        "alias",
    )

def test_second_batch_aliases():
    cases = {
        "Homarine HCI": "homarine hcl",
        "Hordeum Vulgare (Barley) Extract\\Extrait D'Orge":
            "hordeum vulgare (barley) extract",
        "Fragrance/Parfum": "fragrance",
    }

    for raw_token, expected_name in cases.items():
        assert normalize_ingredient(raw_token) == (
            expected_name,
            "alias",
        )