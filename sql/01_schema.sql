CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.products_raw (
    product_id text PRIMARY KEY,
    product_name_raw text NOT NULL,
    brand_raw text NOT NULL,
    product_name_norm text NOT NULL,
    brand_norm text NOT NULL,
    category text NOT NULL,
    product_form text NOT NULL,
    source_name text NOT NULL,
    source_type text NOT NULL,
    source_url text NOT NULL,
    date_accessed date NOT NULL,
    raw_ingredient_list text NOT NULL,
    price numeric NOT NULL,
    currency text NOT NULL,
    size_value numeric NOT NULL,
    size_unit text NOT NULL,
    price_per_unit numeric NOT NULL,
    data_notes text,
    ingested_at timestamptz NOT NULL DEFAULT now()
);