import pandas as pd
from sqlalchemy import text

from src.db import ENGINE


PRODUCT_COLUMNS = [
    "product_id",
    "product_name_raw",
    "brand_raw",
    "product_name_norm",
    "brand_norm",
    "category",
    "product_form",
    "source_name",
    "source_type",
    "source_url",
    "date_accessed",
    "raw_ingredient_list",
    "price",
    "currency",
    "size_value",
    "size_unit",
    "price_per_unit",
    "data_notes",
]

products = pd.read_excel(
    "data/raw/BeautyGraph_Dataset.xlsx",
    sheet_name="Products",
    usecols=PRODUCT_COLUMNS,
)

with ENGINE.begin() as connection:
    connection.execute(text("DELETE FROM raw.products_raw"))

    products.to_sql(
        "products_raw",
        connection,
        schema="raw",
        if_exists="append",
        index=False,
    )

print(f"Imported {len(products)} products.")