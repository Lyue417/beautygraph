CREATE TABLE IF NOT EXISTS raw.product_ingredients_raw (
    product_id text NOT NULL
        REFERENCES raw.products_raw(product_id)
        ON DELETE CASCADE,
    ingredient_position integer NOT NULL,
    raw_token text NOT NULL,
    parser_version text NOT NULL,
    parsed_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (product_id, ingredient_position)
);