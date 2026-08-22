# BeautyGraph Data Model and Data Dictionary

## 1. Purpose

BeautyGraph uses a relational PostgreSQL data model to represent skincare products, ordered ingredient lists, normalized ingredients, and ingredient functions.

The core logical relationship is:

```text
Product
   │
   │ contains ingredient
   │ with list position
   ▼
Ingredient
   │
   │ has function
   ▼
Function
```

This structure provides the data layer used by the similarity engine, formula-function profiles, explanations, and prototype interface.

The current implementation uses PostgreSQL rather than a separate graph database. However, the relational schema directly represents a product–ingredient–function graph and can be interpreted as nodes and edges.

---

## 2. Data Layers

BeautyGraph separates source data from normalized data.

### Raw layer

The `raw` schema preserves source-level product and ingredient information.

Main tables:

- `raw.products_raw`
- `raw.product_ingredients_raw`

### Normalized layer

The `normalized` schema stores standardized ingredient identities and ingredient-function relationships.

Main tables:

- `normalized.ingredients`
- `normalized.product_ingredients`
- `normalized.functions`
- `normalized.ingredient_functions`

The processing flow is:

```text
raw.products_raw
        │
        ▼
raw.product_ingredients_raw
        │
        ▼
normalized.product_ingredients
        │
        ├──────────────► normalized.ingredients
        │
        ▼
normalized.ingredient_functions
        │
        ▼
normalized.functions
```

---

## 3. Core Entity Dictionary

### 3.1 Product

A product represents one leave-on facial moisturizer in the frozen BeautyGraph dataset.

Primary identifier:

`product_id`

Current dataset scope:

- 50 products
- one skincare category: leave-on facial moisturizers
- multiple product forms including cream, gel cream, lotion, balm, fluid, gel, and milk

Product information is stored in:

`raw.products_raw`

### 3.2 Ingredient

An Ingredient represents one canonical normalized ingredient identity.

Examples:

```text
water
glycerin
dimethicone
niacinamide
ceramide np
```

Different observed source names can be normalized to the same canonical ingredient.

Ingredient identity is stored in:

`normalized.ingredients`

### 3.3 Function

A Function represents one controlled ingredient-function group used by BeautyGraph.

The current taxonomy contains 10 groups:

```text
humectant
emollient
occlusive
barrier_supporting
soothing
antioxidant
texture_viscosity
preservative
fragrance_related
active_treatment
```

Function definitions are documented separately in:

`03_ingredient_function_taxonomy.md`

Function records are stored in:

`normalized.functions`

---

## 4. Relationship Model

### 4.1 Product → Ingredient

A product contains an ordered list of ingredients.

This relationship is represented by:

`normalized.product_ingredients`

Conceptually:

```text
(Product)-[CONTAINS]->(Ingredient)
```

The relationship also contains important metadata:

```text
ingredient_position
raw_token
normalization_method
normalizer_version
```

The `ingredient_position` preserves published ingredient-list order and is used by the position-weighted similarity model.

A product may contain many ingredients.

An ingredient may appear in many products.

Therefore:

```text
Product  M:N  Ingredient
```

with `normalized.product_ingredients` acting as the relationship table.

### 4.2 Ingredient → Function

An ingredient can be mapped to one or more functions.

This relationship is represented by:

`normalized.ingredient_functions`

Conceptually:

```text
(Ingredient)-[HAS_FUNCTION]->(Function)
```

Relationship metadata includes:

```text
source
confidence
mapping_version
notes
mapped_at
```

An ingredient can have multiple functions.

A function can be associated with many ingredients.

Therefore:

```text
Ingredient  M:N  Function
```

---

## 5. Graph Schema

The logical BeautyGraph graph schema is:

```text
┌─────────────────────┐
│       Product       │
│---------------------│
│ product_id          │
│ product_name        │
│ brand               │
│ category            │
│ product_form        │
└──────────┬──────────┘
           │
           │ CONTAINS
           │
           │ ingredient_position
           │ raw_token
           │ normalization_method
           │ normalizer_version
           ▼
┌─────────────────────┐
│     Ingredient      │
│---------------------│
│ ingredient_id       │
│ normalized_name     │
└──────────┬──────────┘
           │
           │ HAS_FUNCTION
           │
           │ source
           │ confidence
           │ mapping_version
           │ notes
           ▼
┌─────────────────────┐
│      Function       │
│---------------------│
│ function_id         │
│ function_name       │
│ description         │
└─────────────────────┘
```

The most important traversal used by BeautyGraph is:

```text
Product
→ ordered ingredients
→ normalized ingredient identities
→ mapped functions
→ formula-function profile
→ similarity and explanation
```

---

## 6. Table Data Dictionary

### 6.1 `raw.products_raw`

Stores the source-level record for each product.

| Field | Type | Meaning |
|---|---|---|
| `product_id` | text | Stable BeautyGraph product identifier and primary key |
| `product_name_raw` | text | Product name as collected from the source |
| `brand_raw` | text | Brand name as collected from the source |
| `product_name_norm` | text | Cleaned product name used by the project |
| `brand_norm` | text | Cleaned brand name |
| `category` | text | Product category |
| `product_form` | text | Product form such as cream, lotion, gel cream, balm, fluid, gel, or milk |
| `source_name` | text | Name of the source from which product information was collected |
| `source_type` | text | Type of source |
| `source_url` | text | Source page URL |
| `date_accessed` | date | Date the source was accessed |
| `raw_ingredient_list` | text | Complete ingredient-list text before parsing |
| `price` | numeric | Recorded product price |
| `currency` | text | Currency associated with the price |
| `size_value` | numeric | Recorded package size |
| `size_unit` | text | Unit associated with package size |
| `price_per_unit` | numeric | Calculated price per unit |
| `data_notes` | text | Optional notes about the collected product record |
| `ingested_at` | timestamptz | Time the record was loaded into PostgreSQL |

`product_id` is the primary key.

Price and package-size fields are retained as source data but are not used by the current similarity engine.

### 6.2 `raw.product_ingredients_raw`

Stores the parsed ingredient tokens from each product's source ingredient list.

| Field | Type | Meaning |
|---|---|---|
| `product_id` | text | Product containing the ingredient token |
| `ingredient_position` | integer | Position of the ingredient in the published list |
| `raw_token` | text | Ingredient text produced by the parser |
| `parser_version` | text | Parser version used to produce the record |
| `parsed_at` | timestamptz | Time the ingredient list was parsed |

Primary key:

```text
(product_id, ingredient_position)
```

Foreign key:

```text
product_id
→ raw.products_raw.product_id
```

This table preserves the ordered parsed representation before ingredient normalization.

### 6.3 `normalized.ingredients`

Stores the controlled canonical ingredient identities.

| Field | Type | Meaning |
|---|---|---|
| `ingredient_id` | bigserial | Internal ingredient identifier and primary key |
| `normalized_name` | text | Unique canonical ingredient name |
| `created_at` | timestamptz | Time the canonical ingredient record was created |

`normalized_name` is unique.

The controlled ingredient dictionary delivered separately in:

`02_controlled_ingredient_dictionary.csv`

provides a review-friendly export of this normalized ingredient layer and its observed source variants.

### 6.4 `normalized.product_ingredients`

Connects products to canonical ingredients while preserving ingredient-list order and normalization provenance.

| Field | Type | Meaning |
|---|---|---|
| `product_id` | text | Product containing the ingredient |
| `ingredient_position` | integer | Published ingredient-list position |
| `ingredient_id` | bigint | Canonical ingredient identifier |
| `raw_token` | text | Original parsed ingredient token |
| `normalization_method` | text | Method used to produce the canonical ingredient name |
| `normalizer_version` | text | Version of the normalization logic |
| `normalized_at` | timestamptz | Time the normalized record was created |

Primary key:

```text
(product_id, ingredient_position)
```

Foreign keys:

```text
product_id
→ raw.products_raw.product_id

ingredient_id
→ normalized.ingredients.ingredient_id
```

This is the main Product–Ingredient relationship table used by downstream analysis.

### 6.5 `normalized.functions`

Stores the controlled BeautyGraph function taxonomy.

| Field | Type | Meaning |
|---|---|---|
| `function_id` | serial | Internal function identifier and primary key |
| `function_name` | text | Unique controlled function-group name |
| `description` | text | Short definition of the function group |

The current implementation contains 10 controlled function groups.

### 6.6 `normalized.ingredient_functions`

Connects canonical ingredients to controlled function groups.

| Field | Type | Meaning |
|---|---|---|
| `ingredient_id` | bigint | Canonical ingredient identifier |
| `function_id` | integer | Controlled function identifier |
| `source` | text | Source or basis used for the mapping |
| `confidence` | text | Mapping confidence |
| `mapping_version` | text | Version of the ingredient-function mapping |
| `notes` | text | Optional mapping notes |
| `mapped_at` | timestamptz | Time the mapping record was created |

Primary key:

```text
(ingredient_id, function_id)
```

Foreign keys:

```text
ingredient_id
→ normalized.ingredients.ingredient_id

function_id
→ normalized.functions.function_id
```

Because the primary key contains both identifiers, one ingredient can be connected to multiple functions without duplicating the same ingredient-function pair.

---

## 7. Identifier and Integrity Rules

### Product identity

Each product has one stable text identifier:

```text
P00001
P00002
...
```

The identifier is preserved across raw, normalized, similarity, evaluation, and prototype layers.

### Ingredient identity

Each normalized ingredient has one canonical `ingredient_id` and one unique `normalized_name`.

Different raw ingredient strings may resolve to the same normalized ingredient.

### Ingredient order

Ingredient position is stored explicitly rather than inferred later.

For each product:

```text
1, 2, 3, ... N
```

represents the published list order.

The compound primary key:

```text
(product_id, ingredient_position)
```

prevents two ingredients from occupying the same position within one product.

### Function identity

Function names are controlled and unique.

Ingredient-function mappings use the controlled function table rather than free-text function labels.

---

## 8. How the Model Supports Similarity

The data model supports three separate comparison signals.

### Ingredient Overlap

Uses canonical ingredient identities from:

```text
normalized.product_ingredients
→ normalized.ingredients
```

This allows the system to compare products even when source ingredient strings originally differed.

### Formula Similarity

Uses:

```text
product_id
ingredient_id
ingredient_position
```

Ingredient position is used to give more influence to ingredients appearing earlier in the published ingredient list.

### Function Similarity

Uses:

```text
Product
→ Ingredient
→ Function
```

to construct a function profile for each product from mapped ingredient-function relationships.

These signals remain separate so the prototype can explain why two formulas may:

- share exact ingredients,
- have similar or different ingredient structures,
- or use different ingredients that serve similar overall functions.

---

## 9. Example Traversal

A simplified example is:

```text
Product:
Calm + Restore Oat Gel Moisturizer

        │
        ├── glycerin
        │      ├── Humectant
        │      └── Texture / viscosity
        │
        ├── dimethicone
        │      └── Emollient
        │
        └── panthenol
               ├── Humectant
               ├── Barrier supporting
               └── Soothing
```

This type of traversal allows BeautyGraph to explain both ingredient-level and function-level product relationships.

---

## 10. Implementation Files

The canonical database schema is defined in:

```text
sql/01_schema.sql
sql/02_parsed_ingredients.sql
sql/03_normalized_ingredients.sql
sql/04_ingredient_functions.sql
```

The final cleaned product-ingredient dataset is delivered as:

```text
01_cleaned_product_ingredient_dataset.csv
```

The controlled ingredient dictionary is delivered as:

```text
02_controlled_ingredient_dictionary.csv
```

The ingredient function taxonomy is documented in:

```text
03_ingredient_function_taxonomy.md
```

Together these files document the main BeautyGraph data layer from source product data through normalized ingredients and ingredient functions.

---

## 11. Scope and Limitations

The graph represents structured relationships derived from published ingredient lists.

It does not represent:

- exact ingredient concentration,
- chemical reaction or formulation process,
- clinical efficacy,
- safety for an individual user,
- ingredient compatibility,
- or causal biological effects.

The Product–Ingredient–Function relationships are intended to support transparent information retrieval, formula comparison, and prototype explanation within the scoped moisturizer dataset.
