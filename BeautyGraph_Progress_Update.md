# BeautyGraph_Progress_Update

# BeautyGraph Progress Update

## Project Scope

The prototype focuses on one category, facial moisturizers, and implements the core data layer needed for explainable product comparison:

```
Product
→ Ingredient
→ Ingredient Function
→ Formula Similarity
→ Explanation
```

The current 16 products are a seed dataset used to validate the pipeline.

## Completed Work

### Data Model and Schema

- Reviewed and simplified the product dataset structure.
- Replaced `subcategory` with `product_form` so the field represents observable formats such as `cream`, `lotion`, `gel_cream`, `balm`, and `fluid`.
- Removed `primary_archetype` and `archetype_note` from the manually maintained product data. Formula archetypes are derived interpretations rather than source facts and are not required for the baseline similarity method.
- Established separate PostgreSQL layers for raw and normalized data.
- Created tables for raw products, parsed product ingredients, normalized ingredients, product–ingredient relationships, function groups, and ingredient–function mappings.

### Product Data Ingestion

- Imported 16 facial moisturizer products into PostgreSQL.
- Preserved source information, raw ingredient lists, product form, price, size, and product-level notes.
- Confirmed that product identifiers and source data remain traceable through the pipeline.

### Ingredient Parsing

- Implemented an ingredient parser that converts each raw ingredient list into ordered ingredient records.
- Preserved ingredient position for later position-aware similarity calculations.
- Handled observed formatting cases including parentheses, slash compounds, inconsistent spacing, trailing punctuation, and ingredient names containing commas.
- Added automated parser tests before normalization to prevent parsing errors from propagating into later stages.

**Result:** 16 products were parsed into **590 product–ingredient records**.

### Ingredient Normalization

- Implemented normalization for case and whitespace differences.
- Added explicit aliases for confirmed equivalent names, including water/aqua variants and fragrance/parfum variants.
- Kept chemically distinct but visually similar names separate.
- Added automated normalization tests.
- Stored the raw token, normalized value, normalization method, and normalizer version for traceability.

### Normalization Quality Review

- Verified that all parsed records map to a valid normalized ingredient.
- Confirmed that there are no empty normalized names or missing ingredient references.
- Reviewed the 100 most frequent normalized ingredients for unresolved duplicates.
- Identified and corrected one malformed source value:

```
Diso- Dium Edta → disodium edta
```

**Current result:**

- **590** product–ingredient records
- **303** unique normalized ingredients
- **0** missing ingredient references
- **0** empty normalized names

### Ingredient Function Taxonomy Structure

Created the first database-level function vocabulary for moisturizer comparison:

- `humectant`
- `emollient`
- `occlusive`
- `barrier_supporting`
- `soothing`
- `antioxidant`
- `texture_viscosity`
- `preservative`
- `fragrance_related`
- `active_treatment`

The mapping structure supports multiple functions per ingredient and records source, confidence, mapping version, and notes.

## Key Implementation Decisions

- PostgreSQL is used as the primary processing layer. Graph database is not required for the current prototype because product–ingredient–function relationships can be represented directly through relational tables.
- Parsing and normalization are separate steps so formatting errors and identity-resolution errors can be tested and corrected independently.
- Ingredient normalization is conservative. Only confirmed aliases are merged; broad fuzzy matching is avoided because similar-looking INCI names may represent different ingredients.
- Formula archetypes are excluded from the source dataset and baseline score. They may be generated later as versioned derived outputs if they add clear value.

## Current Status

The project now has a reproducible pipeline from product records to normalized ordered ingredients:

```
Product dataset
→ raw products
→ ingredient parser
→ parsed ingredient records
→ ingredient normalizer
→ normalized ingredients
→ normalized product–ingredient relationships
```

The data foundation is ready for dataset expansion and ingredient-function mapping.

## Next Steps

1. **Expand the product dataset in batches.**
    
    Add 10–20 products per batch and run them through the existing ingestion, parsing, normalization, and quality-review pipeline. The target is approximately 80–100 products.
    
2. **Validate ingredient identity and build the function mapping.**
    
    Use INCI naming references and sources such as PCPC/INCI, EU CosIng, and COSMILE Europe to confirm canonical ingredient names, aliases, and cosmetic functions. These sources will support the ingredient layer; the project-specific function groups will remain the controlled taxonomy used by BeautyGraph. Mapping will prioritize frequent and high-position ingredients and will be updated as new products are added.
    
3. **Implement the first similarity baseline after sufficient product coverage.**
    
    The initial model will use normalized ingredient overlap, position-weighted ingredient similarity, and ingredient-function similarity. The output will be reviewed through top-k product comparisons before interface development.