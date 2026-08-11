import re

import pandas as pd
from sqlalchemy import text

from src.db import ENGINE


PARSER_VERSION = "v2"


def parse_ingredient_list(raw_text: str) -> list[str]:
    text = raw_text.replace("\r", "\n")

    # Protect commas inside parentheses, e.g. AQUA (WATER, EAU).
    text = re.sub(
        r"\([^()]*\)",
        lambda match: match.group(0).replace(",", "<PROTECTED_COMMA>"),
        text,
    )

    # Protect numeric commas, e.g. 1,2-Hexanediol.
    text = re.sub(
        r"(?<=\d),(?=\d)",
        "<PROTECTED_COMMA>",
        text,
    )

    # If another explicit delimiter exists, treat newlines as formatting wraps.
    has_explicit_separator = (
        "•" in text
        or "･" in text
        or re.search(r"\s+-\s+", text) is not None
        or "," in text
        or ". " in text
    )

    text = text.replace(
        "\n",
        " " if has_explicit_separator else "•",
    )
    text = re.sub(r"\s+", " ", text)

    tokens = re.split(
        r"[•･,]+|\s+-\s+|\.\s+",
        text,
    )

    return [
        token.replace("<PROTECTED_COMMA>", ",").strip().rstrip(".")
        for token in tokens
        if token.replace("<PROTECTED_COMMA>", ",").strip().rstrip(".")
    ]


def main() -> None:
    products = pd.read_sql(
        """
        SELECT product_id, raw_ingredient_list
        FROM raw.products_raw
        ORDER BY product_id
        """,
        ENGINE,
    )

    rows = []

    for product in products.itertuples(index=False):
        ingredients = parse_ingredient_list(product.raw_ingredient_list)

        for position, raw_token in enumerate(ingredients, start=1):
            rows.append(
                {
                    "product_id": product.product_id,
                    "ingredient_position": position,
                    "raw_token": raw_token,
                    "parser_version": PARSER_VERSION,
                }
            )

    parsed = pd.DataFrame(rows)

    with ENGINE.begin() as connection:
        connection.execute(text("TRUNCATE TABLE raw.product_ingredients_raw"))

        parsed.to_sql(
            "product_ingredients_raw",
            connection,
            schema="raw",
            if_exists="append",
            index=False,
        )

    print(
        f"Parsed {len(products)} products "
        f"into {len(parsed)} ingredient records."
    )


if __name__ == "__main__":
    main()