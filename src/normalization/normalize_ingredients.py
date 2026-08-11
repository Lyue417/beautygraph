import re


NORMALIZER_VERSION = "v5"

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
    "water/aqua": "water",
    "water/eau": "water",
    "water(aqua/eau)": "water",
    "water (aqua) (eau)": "water",
    "water (aqua / eau)": "water",
    "aqua (water, eau)": "water",
    "purified water": "water",
    "fragrance (parfum)": "fragrance",
    "parfum / fragrance": "fragrance",
    "parfum/fragrance": "fragrance",
    "parfum (fragrance)": "fragrance",
    "fragrance/parfum": "fragrance",
    "cetearylalcohol": "cetearyl alcohol",
    "diso- dium edta": "disodium edta",
    "homarine hci": "homarine hcl",
    "hordeum vulgare (barley) extract\\extrait d'orge":
    "hordeum vulgare (barley) extract",
    "butyrospermum parkii (shea) butter":
    "butyrospermum parkii butter",
    "butyrospermum parkii butter / shea butter":
    "butyrospermum parkii butter",
    "cera microcristallina / microcrystalline wax":
    "microcrystalline wax",
    "microcrystalline wax\\cera microcristallina\\cire microcristalline":
    "microcrystalline wax",
    "helianthus annuus seed oil/sunflower seed oil":
    "helianthus annuus seed oil",
    "helianthus annuus (sunflower) seed oil":
    "helianthus annuus seed oil",
    "mineral oil\\paraffinum liquidum\\huile minerale": "mineral oil",
    "mineral oil\\paraffinum liquidum\\huile minérale": "mineral oil",
    "glycine soja oil/soybean oil":
    "glycine soja oil",
    "glycine soja (soybean) oil": "glycine soja oil",
    "chamomilla recutita flower extract/matricaria flower extract":
    "chamomilla recutita flower extract",
    "medicago sativa extract/alfalfa extract":
    "medicago sativa extract",
    "spinacia oleracea/spinach leaf extract":
    "spinacia oleracea leaf extract",
    "zea mays starch / corn starch":
    "zea mays starch",
    "eucalyptus globulus (eucalyptus) leaf oil":
    "eucalyptus globulus leaf oil",
    "xanthamgum": "xanthan gum",
    "rosmarinus officinalis (rosemary) leaf extract (rosmarinus officinalis leaf extract)":
    "rosmarinus officinalis (rosemary) leaf extract",

}


def simplify_token(raw_token: str) -> str:
    return re.sub(r"\s+", " ", raw_token.strip()).lower()


def normalize_ingredient(raw_token: str) -> tuple[str, str]:
    simplified = simplify_token(raw_token)

    if simplified in ALIASES:
        return ALIASES[simplified], "alias"

    return simplified, "case_whitespace"