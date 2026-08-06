import re


NORMALIZER_VERSION = "v2"

ALIASES = {
    "water": "water",
    "aqua": "water",
    "aqua (water)": "water",
    "water (aqua)": "water",
    "aqua / water": "water",
    "aqua / water / eau": "water",
    "aqua/water/eau": "water",
    "water/aqua/eau": "water",
    "water\\aqua\\eau": "water",
    "fragrance (parfum)": "fragrance",
    "parfum / fragrance": "fragrance",
    "parfum/fragrance": "fragrance",
    "fragrance/parfum": "fragrance",
    "diso- dium edta": "disodium edta",
    "homarine hci": "homarine hcl",
    "hordeum vulgare (barley) extract\\extrait d'orge": "hordeum vulgare (barley) extract",
}


def simplify_token(raw_token: str) -> str:
    return re.sub(r"\s+", " ", raw_token.strip()).lower()


def normalize_ingredient(raw_token: str) -> tuple[str, str]:
    simplified = simplify_token(raw_token)

    if simplified in ALIASES:
        return ALIASES[simplified], "alias"

    return simplified, "case_whitespace"