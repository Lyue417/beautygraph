import pandas as pd


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

print("Rows:", len(products))
print("Columns:", products.columns.tolist())
print("Duplicate product IDs:", products["product_id"].duplicated().sum())
print("Missing values:")
print(products.isna().sum())