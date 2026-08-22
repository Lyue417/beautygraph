# BeautyGraph Baseline Formula Similarity Module

## 1. Purpose

This deliverable documents the baseline formula-similarity module implemented for BeautyGraph.

The canonical implementation remains in the project source code rather than being duplicated in this folder.

Main implementation files:

- `src/similarity/metrics.py`
- `src/similarity/engine.py`
- `src/similarity/comparison.py`

Related tests:

- `tests/test_similarity.py`
- `tests/test_similarity_engine.py`
- `tests/test_comparison.py`

The module compares products using three separate, explainable similarity signals rather than one opaque combined score.

---

## 2. Inputs

The similarity engine reads normalized product and ingredient data from PostgreSQL.

For each product, the engine loads:

- `product_id`
- brand
- product name
- product form
- normalized ingredient IDs
- normalized ingredient names
- published ingredient-list positions

It also loads ingredient-to-function mappings from the controlled function taxonomy.

The main data path is:

```text
Product
→ normalized ingredients
→ ingredient positions
→ mapped functions
→ similarity signals
```

The engine builds the following structures for each product:

```text
ingredient_set
positions
ingredient_names
function_profile
formula_profile
function_mapping_coverage
```

---

## 3. Similarity Signals

BeautyGraph keeps three similarity signals separate.

### 3.1 Ingredient Overlap

**Question answered:** How many normalized ingredients do the two products share?

Implementation:

`jaccard_similarity()`

Formula:

```text
Ingredient Overlap
=
|A ∩ B|
────────
|A ∪ B|
```

where:

- `A` is the set of normalized ingredients in Product A
- `B` is the set of normalized ingredients in Product B

The result ranges from 0 to 1.

Examples:

```text
0.00 = no normalized ingredients shared
1.00 = the normalized ingredient sets are identical
```

Ingredient position is not used in this metric.

---

### 3.2 Formula Similarity

**Question answered:** Do the products share ingredients in similarly important positions of their published ingredient lists?

Implementation:

- `position_weight()`
- `weighted_jaccard_similarity()`

Each ingredient receives a position weight:

```text
weight(position) = 1 / √position
```

Examples:

```text
Position 1  → 1.000
Position 4  → 0.500
Position 9  → 0.333
Position 16 → 0.250
```

Ingredients appearing earlier in the published ingredient list therefore receive more influence.

For each normalized ingredient, the engine compares its weight in both products.

The weighted Jaccard score is:

```text
Formula Similarity
=
Σ min(weightA, weightB)
────────────────────────
Σ max(weightA, weightB)
```

An ingredient missing from one product receives weight 0 for that product.

The result ranges from 0 to 1.

This is the primary ranking score used by the **Similar Products** feature.

---

### 3.3 Function Similarity

**Question answered:** Do the mapped ingredients in the two formulas play similar overall functional roles?

Implementation:

- `build_function_profile()`
- `cosine_similarity()`

The controlled function groups are:

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

For each ingredient with at least one mapped function:

```text
ingredient contribution
=
position weight
───────────────
number of mapped functions
```

If an ingredient has multiple mapped functions, its position-weighted contribution is divided equally across those groups.

Example:

```text
Panthenol
Position-weighted contribution = 0.40

Mapped functions:
- humectant
- barrier_supporting
- soothing

Contribution to each group:
0.40 / 3
```

The contributions are summed across all mapped ingredients to create a function vector.

Function Similarity is calculated with cosine similarity:

```text
                 A · B
cosine(A, B) = ─────────
               ||A|| ||B||
```

A high score means the relative direction of the two mapped function patterns is similar.

Different ingredients can therefore produce high Function Similarity when they perform similar types of roles.

---

## 4. Formula Function Profile

BeautyGraph also creates a normalized Function Profile for display and explanation.

Implementation:

`normalize_function_profile()`

The raw function contributions are divided by their total:

```text
normalized function share
=
function contribution
─────────────────────
total mapped contribution
```

The normalized profile therefore sums to 1.0 before display rounding.

In the prototype, it is shown as percentages that together make up 100% of the mapped Function Profile.

These percentages are **not ingredient concentrations**.

---

## 5. Function Mapping Coverage

Not every normalized ingredient currently has a controlled function mapping.

Implementation:

`function_mapping_coverage()`

Coverage is calculated as:

```text
Function Mapping Coverage
=
total position-weighted contribution of mapped ingredients
──────────────────────────────────────────────────────────
total position weight of all ingredients in the product
```

This value answers:

> How much of the position-weighted ingredient-list structure is represented in the current function mapping?

An unmapped ingredient:

- still appears in the normalized ingredient list;
- still contributes to Ingredient Overlap;
- still contributes to Formula Similarity;
- but does not contribute to the Function Profile or Function Similarity.

---

## 6. Pairwise Comparison

Implementation:

`compute_pair_components()`

For any pair of products, the engine returns:

```text
ingredient_similarity
formula_similarity
function_similarity
```

Example structure:

```json
{
  "ingredient_similarity": 0.56,
  "formula_similarity": 0.57,
  "function_similarity": 0.97
}
```

The three scores are intentionally not combined.

This preserves interpretability because each signal answers a different question.

---

## 7. All-Pairs Calculation

Implementation:

`compute_all_pairs()`

The engine calculates every unique pair of products.

For a frozen dataset of 50 products:

```text
50 × 49
─────── = 1,225 unique product pairs
   2
```

Each pair is evaluated once.

The result contains:

```text
product_a_id
product_b_id
ingredient_similarity
formula_similarity
function_similarity
```

---

## 8. Top-5 Similar Products

Implementation:

`get_top_similar_products()`

For a selected product, the engine:

1. retrieves all product pairs involving that product;
2. identifies the other product in each pair;
3. keeps all three similarity signals;
4. sorts candidates by `formula_similarity` in descending order;
5. returns the first five results.

Conceptually:

```text
Selected product
      │
      ▼
All 49 candidate products
      │
      ▼
Compute / retrieve similarity signals
      │
      ▼
Sort by Formula Similarity
      │
      ▼
Top 5
```

Ingredient Overlap and Function Similarity are shown as supporting signals but do not determine the ranking.

---

## 9. Comparison Features

The similarity module also produces explanation-ready comparison data.

Implementation:

`src/similarity/comparison.py`

### Ingredient comparison

`compare_ingredients()` identifies:

- all shared normalized ingredients;
- shared ingredients appearing within the first 10 positions of both lists;
- ingredients only in Product A;
- ingredients only in Product B.

Shared ingredients are ordered using ingredient-list position so that high-position overlap is surfaced first.

### Function comparison

`compare_functions()` identifies:

- function groups present in both mapped profiles;
- each product's share of each function group;
- the absolute difference between the two function profiles by group.

These features support the Compare Products interface and deterministic explanations.

---

## 10. Why Formula Similarity Is the Ranking Signal

The prototype uses Formula Similarity rather than Ingredient Overlap alone because exact overlap treats all ingredients equally.

For example:

```text
Shared ingredient at position 2
```

and:

```text
Shared ingredient at position 35
```

would contribute equally to ordinary Jaccard overlap.

The position-weighted model instead gives more influence to ingredients appearing earlier in the published list.

Function Similarity is retained as a separate explanatory signal because two formulas can use different ingredients while still having similar mapped functional patterns.

The manual similarity review also found that the highest-ranked Formula Similarity results were generally reasonable within the reviewed sample.

---

## 11. Interpretation Example

A pair may produce:

```text
Formula Similarity:    6%
Ingredient Overlap:    6%
Function Similarity:  96%
```

This does not mean the scores conflict.

It means:

- the two formulas share few exact normalized ingredients;
- their shared ingredients do not align strongly in high-position formula structure;
- but the ingredients that BeautyGraph can map are distributed across very similar function groups.

In plain language:

> Different ingredient structures can still perform similar overall roles.

This separation is central to BeautyGraph's explainability approach.

---

## 12. Deterministic Design

The baseline similarity system is deterministic.

Given the same:

- normalized ingredient identities;
- ingredient positions;
- function mappings;
- and algorithm version,

the same product pair produces the same scores.

There is no machine-learning model, embedding model, or generative model in the similarity ranking itself.

This was intentional for the practicum prototype because the main project goal was to build a transparent and inspectable formula-comparison system.

---

## 13. Testing

Similarity behavior is covered by project tests.

Relevant test files are:

```text
tests/test_similarity.py
tests/test_similarity_engine.py
tests/test_comparison.py
```

These tests cover the similarity metrics, engine behavior, and comparison feature generation.

The final prototype was also checked across the complete frozen 50-product serving dataset to confirm:

- 50 products were present;
- 1,225 unique pair comparisons were available;
- each product had five ranked similar-product results;
- Top-5 results were ordered by Formula Similarity;
- similarity values remained between 0 and 1.

Manual similarity review results are documented separately in:

`07_evaluation_summary.md`

---

## 14. Canonical Implementation

The canonical implementation is kept in the original source-code locations:

```text
src/similarity/metrics.py
src/similarity/engine.py
src/similarity/comparison.py
```

This deliverable is the review-friendly documentation and index for that implemented baseline module.

The module should not be duplicated into a separate notebook because doing so would create a second implementation that could diverge from the tested project code.

---

## 15. Scope and Limitations

The similarity module compares structured published ingredient-list information.

It does not estimate:

- exact ingredient concentrations;
- manufacturing process;
- formulation stability;
- texture equivalence;
- clinical efficacy;
- safety for a specific person;
- medical suitability.

Ingredient-list order is used as an approximation of formula structure, not as a direct measurement of concentration.

Function Similarity is also limited by current ingredient-function mapping coverage.

The module is therefore best interpreted as an explainable baseline for formula-relationship exploration within the scoped BeautyGraph dataset.
