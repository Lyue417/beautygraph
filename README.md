# BeautyGraph

**Explainable skincare formula similarity and comparison prototype**

[Live Demo](https://lyue417.github.io/beautygraph/)

BeautyGraph is an information-system prototype for exploring relationships between skincare products through normalized ingredients, ingredient functions, and transparent formula-similarity signals.

The current prototype focuses on a frozen dataset of **50 leave-on facial moisturizers**.

## What BeautyGraph Does

BeautyGraph connects:

```text
Product
→ Ingredient
→ Ingredient Function
→ Formula Similarity
→ Explanation
```

The system supports three main user flows.

### Product Profile

Explore an individual product's:

- normalized ingredient list;
- ingredient-list order;
- mapped ingredient-function coverage;
- position-weighted Formula Function Profile.

### Compare Products

Compare any two products using:

- normalized ingredient overlap;
- position-weighted ingredient similarity;
- function-profile similarity;
- shared and product-specific ingredients;
- shared high-position ingredients;
- largest function-profile differences;
- deterministic explanations of the relationship.

### Similar Products

Select a product and view its Top-5 closest formulas.

Results are ranked by position-weighted ingredient similarity, with ingredient overlap and mapped function similarity shown as supporting signals.

## Similarity Approach

BeautyGraph currently uses three transparent similarity signals:

1. **Normalized ingredient overlap**  
   Measures exact overlap between normalized ingredient sets.

2. **Position-weighted ingredient similarity**  
   Gives more weight to ingredients appearing earlier in the published ingredient list.

3. **Function-profile similarity**  
   Compares the relative distribution of mapped ingredient-function signals.

The current prototype keeps these signals separate rather than combining them into an opaque overall score.

## Data Pipeline

The project uses PostgreSQL and Python for the processing pipeline:

```text
Raw product data
→ ingestion
→ ingredient parsing
→ ingredient normalization
→ ingredient-function mapping
→ similarity
→ comparison features
→ deterministic explanation
```

The public demo uses an exported frozen serving dataset generated from this pipeline, allowing the interface to run as a static website without requiring a live database.

## Prototype

The working prototype includes:

- Product Profile
- Compare Products
- Similar Products
- explainable comparison results
- generic watercolor product-form illustrations
- responsive browser-based interface

The public demo is hosted through GitHub Pages:

**https://lyue417.github.io/beautygraph/**

## Technology

- Python
- PostgreSQL
- SQLAlchemy
- pytest
- Streamlit for local prototype development
- HTML / CSS / JavaScript for the public demo
- GitHub Pages for public deployment

## Current Scope

BeautyGraph currently focuses on leave-on facial moisturizers.

The dataset is intentionally scoped and frozen for prototype development and evaluation rather than intended to represent the entire skincare market.

## Limitations

BeautyGraph analyzes structured ingredient-list relationships.

Similarity results do **not** establish:

- identical ingredient concentrations;
- identical formulation;
- identical texture or stability;
- clinical efficacy;
- safety for a specific individual;
- medical suitability.

Ingredient-function profiles represent mapped formula signals, not ingredient concentrations or efficacy scores.

## Copyright

Copyright © 2026. All rights reserved.

This repository is available for viewing and educational evaluation
only. No license is granted for copying, modification, redistribution,
or commercial use. See [LICENSE.md](LICENSE.md) for details.