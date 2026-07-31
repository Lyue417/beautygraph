import re

import pandas as pd
from sqlalchemy import text

from src.db import ENGINE


PARSER_VERSION = "v1"


def parse_ingredient_list(raw_text: str) -> list[str]:
    text = raw_text.replace("\r", "•").replace("\n", "•")
    text = re.sub(r"\s+", " ", text)

    # Protect commas inside names such as 1,2-Hexanediol.
    text = re.sub(r"(?<=\d),(?=\d)", "<DECIMAL_COMMA>", text)

    tokens = re.split(r"[•,]+", text)

    return [
        token.replace("<DECIMAL_COMMA>", ",").strip().rstrip(".")
        for token in tokens
        if token.replace("<DECIMAL_COMMA>", ",").strip().rstrip(".")
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