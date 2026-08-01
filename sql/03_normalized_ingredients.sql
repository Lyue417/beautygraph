CREATE SCHEMA IF NOT EXISTS normalized;

CREATE TABLE IF NOT EXISTS normalized.ingredients (
    ingredient_id bigserial PRIMARY KEY,
    normalized_name text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS normalized.product_ingredients (
    product_id text NOT NULL
        REFERENCES raw.products_raw(product_id)
        ON DELETE CASCADE,
    ingredient_position integer NOT NULL,
    ingredient_id bigint NOT NULL
        REFERENCES normalized.ingredients(ingredient_id),
    raw_token text NOT NULL,
    normalization_method text NOT NULL,
    normalizer_version text NOT NULL,
    normalized_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (product_id, ingredient_position)
);