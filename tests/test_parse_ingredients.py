from src.parsing.parse_ingredients import parse_ingredient_list


def test_comma_separated_list():
    raw = "Water, Glycerin, Dimethicone"

    assert parse_ingredient_list(raw) == [
        "Water",
        "Glycerin",
        "Dimethicone",
    ]


def test_newline_separated_list():
    raw = "Water\nGlycerin\nCeramide NP"

    assert parse_ingredient_list(raw) == [
        "Water",
        "Glycerin",
        "Ceramide NP",
    ]


def test_bullet_separated_list():
    raw = "Water • Glycerin • Squalane"

    assert parse_ingredient_list(raw) == [
        "Water",
        "Glycerin",
        "Squalane",
    ]


def test_numeric_comma_is_preserved():
    raw = "Water, 1,2-Hexanediol, 2,3-Butanediol"

    assert parse_ingredient_list(raw) == [
        "Water",
        "1,2-Hexanediol",
        "2,3-Butanediol",
    ]


def test_slashes_are_not_split():
    raw = (
        "AQUA / WATER / EAU, "
        "CAPRYLIC/CAPRIC TRIGLYCERIDE, "
        "PARFUM/FRAGRANCE"
    )

    assert parse_ingredient_list(raw) == [
        "AQUA / WATER / EAU",
        "CAPRYLIC/CAPRIC TRIGLYCERIDE",
        "PARFUM/FRAGRANCE",
    ]


def test_backslashes_are_not_split():
    raw = (
        "Mineral Oil\\Paraffinum Liquidum\\Huile Minerale, "
        "Petrolatum"
    )

    assert parse_ingredient_list(raw) == [
        "Mineral Oil\\Paraffinum Liquidum\\Huile Minerale",
        "Petrolatum",
    ]


def test_extra_spaces_and_final_period_are_removed():
    raw = " Water ,   Glycerin  , Phenoxyethanol. "

    assert parse_ingredient_list(raw) == [
        "Water",
        "Glycerin",
        "Phenoxyethanol",
    ]