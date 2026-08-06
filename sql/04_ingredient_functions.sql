CREATE TABLE IF NOT EXISTS normalized.functions (
    function_id serial PRIMARY KEY,
    function_name text NOT NULL UNIQUE,
    description text
);

CREATE TABLE IF NOT EXISTS normalized.ingredient_functions (
    ingredient_id bigint NOT NULL
        REFERENCES normalized.ingredients(ingredient_id)
        ON DELETE CASCADE,
    function_id integer NOT NULL
        REFERENCES normalized.functions(function_id)
        ON DELETE CASCADE,
    source text NOT NULL,
    confidence text NOT NULL,
    mapping_version text NOT NULL,
    notes text,
    mapped_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (ingredient_id, function_id)
);

INSERT INTO normalized.functions (
    function_name,
    description
)
VALUES
    (
        'humectant',
        'Helps attract or retain water.'
    ),
    (
        'emollient',
        'Helps soften and smooth the skin surface.'
    ),
    (
        'occlusive',
        'Helps reduce water loss by forming a surface barrier.'
    ),
    (
        'barrier_supporting',
        'Supports skin barrier structure or lipid composition.'
    ),
    (
        'soothing',
        'Associated with soothing or comfort-supporting functions.'
    ),
    (
        'antioxidant',
        'Helps limit oxidation in the formula or on the skin.'
    ),
    (
        'texture_viscosity',
        'Supports texture, thickening, stabilization, or rheology.'
    ),
    (
        'preservative',
        'Helps protect the product from microbial contamination.'
    ),
    (
        'fragrance_related',
        'Provides fragrance or is associated with fragrance materials.'
    ),
    (
        'active_treatment',
        'Provides a treatment-oriented or targeted cosmetic function.'
    )
ON CONFLICT (function_name) DO NOTHING;