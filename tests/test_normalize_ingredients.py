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

def test_common_name_and_multilingual_aliases():
    cases = {
        "Butyrospermum Parkii (Shea) Butter":
            "butyrospermum parkii butter",
        "BUTYROSPERMUM PARKII BUTTER / SHEA BUTTER":
            "butyrospermum parkii butter",
        "CERA MICROCRISTALLINA / MICROCRYSTALLINE WAX":
            "microcrystalline wax",
        "Microcrystalline Wax\\Cera Microcristallina\\Cire Microcristalline":
            "microcrystalline wax",
        "HELIANTHUS ANNUUS SEED OIL/SUNFLOWER SEED OIL":
            "helianthus annuus seed oil",
        "Helianthus Annuus (Sunflower) Seed Oil":
            "helianthus annuus seed oil",
        "Mineral Oil\\Paraffinum Liquidum\\Huile Minerale":
            "mineral oil",
        "Glycine Soja Oil/Soybean Oil":
            "glycine soja oil",
        "Chamomilla Recutita Flower Extract/Matricaria Flower Extract":
            "chamomilla recutita flower extract",
        "Medicago Sativa Extract/Alfalfa Extract":
            "medicago sativa extract",
        "Spinacia Oleracea/Spinach Leaf Extract":
            "spinacia oleracea leaf extract",
        "Zea Mays Starch / Corn Starch":
            "zea mays starch",
        "Eucalyptus Globulus (Eucalyptus) Leaf Oil":
            "eucalyptus globulus leaf oil",
    }

    for raw_token, expected_name in cases.items():
        assert normalize_ingredient(raw_token) == (
            expected_name,
            "alias",
        )


def test_additional_water_aliases():
    variants = [
        "water/aqua",
        "Water/Eau",
        "WATER(AQUA/EAU)",
        "Water (Aqua) (Eau)",
        "Water (Aqua / Eau)",
        "AQUA (WATER, EAU)",
        "Purified Water",
    ]

    for variant in variants:
        assert normalize_ingredient(variant) == (
            "water",
            "alias",
        )


def test_additional_fragrance_alias():
    assert normalize_ingredient("PARFUM (FRAGRANCE)") == (
        "fragrance",
        "alias",
    )


def test_confirmed_spelling_aliases():
    assert normalize_ingredient("Cetearylalcohol") == (
        "cetearyl alcohol",
        "alias",
    )

    assert normalize_ingredient("Xanthamgum") == (
        "xanthan gum",
        "alias",
    )


def test_soybean_oil_alias():
    assert normalize_ingredient("GLYCINE SOJA (SOYBEAN) OIL") == (
        "glycine soja oil",
        "alias",
    )


def test_repeated_rosemary_extract_alias():
    raw = (
        "ROSMARINUS OFFICINALIS (ROSEMARY) LEAF EXTRACT "
        "(ROSMARINUS OFFICINALIS LEAF EXTRACT)"
    )

    assert normalize_ingredient(raw) == (
        "rosmarinus officinalis (rosemary) leaf extract",
        "alias",
    )


def test_accented_mineral_oil_alias():
    assert normalize_ingredient(
        "Mineral Oil\\Paraffinum Liquidum\\Huile Minérale"
    ) == (
        "mineral oil",
        "alias",
    )