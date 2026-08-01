import pandas as pd
from sqlalchemy import text

from src.db import ENGINE
from src.normalization.normalize_ingredients import (
    NORMALIZER_VERSION,
    normalize_ingredient,
)


def main() -> None:
    raw = pd.read_sql(
        """
        SELECT
            product_id,
            ingredient_position,
            raw_token
        FROM raw.product_ingredients_raw
        ORDER BY product_id, ingredient_position
        """,
        ENGINE,
    )

    rows = []

    for record in raw.itertuples(index=False):
        normalized_name, method = normalize_ingredient(record.raw_token)

        rows.append(
            {
                "product_id": record.product_id,
                "ingredient_position": record.ingredient_position,
                "raw_token": record.raw_token,
                "normalized_name": normalized_name,
                "normalization_method": method,
            }
        )

    normalized = pd.DataFrame(rows)
    unique_names = sorted(normalized["normalized_name"].unique())

    with ENGINE.begin() as connection:
        connection.execute(
            text("TRUNCATE TABLE normalized.product_ingredients")
        )
        connection.execute(
            text(
                "TRUNCATE TABLE normalized.ingredients "
                "RESTART IDENTITY CASCADE"
            )
        )

        connection.execute(
            text(
                """
                INSERT INTO normalized.ingredients (normalized_name)
                SELECT unnest(:names)
                """
            ),
            {"names": unique_names},
        )

        ingredient_ids = pd.read_sql(
            """
            SELECT ingredient_id, normalized_name
            FROM normalized.ingredients
            """,
            connection,
        )

        normalized = normalized.merge(
            ingredient_ids,
            on="normalized_name",
            how="left",
            validate="many_to_one",
        )

        normalized[
            [
                "product_id",
                "ingredient_position",
                "ingredient_id",
                "raw_token",
                "normalization_method",
            ]
        ].assign(
            normalizer_version=NORMALIZER_VERSION
        ).to_sql(
            "product_ingredients",
            connection,
            schema="normalized",
            if_exists="append",
            index=False,
        )

    print(
        f"Normalized {len(normalized)} ingredient records "
        f"into {len(unique_names)} unique ingredients."
    )


if __name__ == "__main__":
    main()