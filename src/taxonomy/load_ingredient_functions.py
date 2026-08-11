import pandas as pd
from sqlalchemy import text

from src.db import ENGINE


MAPPING_PATH = "data/samples/ingredient_function_map.csv"
MAPPING_VERSION = "v2"


def main() -> None:
    mappings = pd.read_csv(MAPPING_PATH)

    required_columns = {
        "normalized_name",
        "function_name",
        "source",
        "confidence",
        "notes",
    }

    if set(mappings.columns) != required_columns:
        raise ValueError("Unexpected mapping file columns.")

    with ENGINE.begin() as connection:
        ingredients = pd.read_sql(
            """
            SELECT ingredient_id, normalized_name
            FROM normalized.ingredients
            """,
            connection,
        )

        functions = pd.read_sql(
            """
            SELECT function_id, function_name
            FROM normalized.functions
            """,
            connection,
        )

        loaded = mappings.merge(
            ingredients,
            on="normalized_name",
            how="left",
            validate="many_to_one",
        ).merge(
            functions,
            on="function_name",
            how="left",
            validate="many_to_one",
        )

        missing_ingredients = loaded.loc[
            loaded["ingredient_id"].isna(),
            "normalized_name",
        ].unique()

        missing_functions = loaded.loc[
            loaded["function_id"].isna(),
            "function_name",
        ].unique()

        if len(missing_ingredients):
            raise ValueError(
                f"Unknown normalized ingredients: "
                f"{sorted(missing_ingredients)}"
            )

        if len(missing_functions):
            raise ValueError(
                f"Unknown function groups: "
                f"{sorted(missing_functions)}"
            )

        connection.execute(
            text("DELETE FROM normalized.ingredient_functions")
        )

        loaded[
            [
                "ingredient_id",
                "function_id",
                "source",
                "confidence",
                "notes",
            ]
        ].assign(
            mapping_version=MAPPING_VERSION
        ).to_sql(
            "ingredient_functions",
            connection,
            schema="normalized",
            if_exists="append",
            index=False,
        )

    print(
        f"Loaded {len(loaded)} function mappings "
        f"for {loaded['ingredient_id'].nunique()} ingredients."
    )

if __name__ == "__main__":
    main()

