# Similarity Engine v1

## Goal

Build a simple and explainable similarity engine for the 50-product moisturizer dataset.

The engine should support three related questions:

1. How much ingredient overlap do two products have?
2. How similar are their formulas when ingredient position is considered?
3. How similar are their mapped functional profiles?

These signals were tested separately before deciding how they should be used in the final system.

---

# 1. Ingredient Similarity

## Decision

Use plain Jaccard similarity to compare normalized ingredient sets.

Formula:

S_ingredient(A, B) =
shared ingredients / all unique ingredients across both products

Example:

If two products share 3 ingredients and have 5 unique ingredients in total:

S_ingredient = 3 / 5 = 0.60

## Why

A raw shared-ingredient count is not enough because products have different ingredient-list lengths.

Jaccard accounts for both shared and different ingredients.

## Final role

Ingredient similarity is kept as:

- a baseline
- a comparison signal
- an explanation feature

It does not independently control the Top-5 ranking.

---

# 2. Ingredient Position Weight

## Decision

Use:

w(position) = 1 / sqrt(position)

Examples:

- position 1 → 1.000
- position 4 → 0.500
- position 9 → 0.333

Earlier ingredients receive more weight, but ingredients later in the list still contribute.

## Important limitation

Ingredient position is only a rank-based proxy.

It does NOT represent exact ingredient concentration.

BeautyGraph would not claim that position weight estimates actual percentages in the formula.

---

# 3. Formula Similarity

## Decision

Use position-weighted generalized Jaccard as Formula Similarity v1.

For each ingredient:

w(p) = 1 / sqrt(position)

For two products:

S_formula(A, B) =
sum(min(w_Ai, w_Bi))
/
sum(max(w_Ai, w_Bi))

This combines:

1. whether the same ingredient appears in both products
2. where that ingredient appears in each ingredient list

## Interpretation

Two products score higher when they:

- share more normalized ingredients
- share ingredients in relatively important positions
- have fewer large ingredient differences

## Final role

`formula_similarity` is the main ranking score for Similar Products.

Top-5 results are sorted only by this score.

---

# 4. Position-Decay Sensitivity Test

The `1 / sqrt(position)` rule is a BeautyGraph v1 design choice.

It was compared against:

1. `1 / sqrt(position)`
2. `1 / log2(position + 1)`
3. `1 / position`

## Results

### sqrt vs log

- score correlation: 0.9974
- average Top-5 overlap: 4.54 / 5
- every product kept at least 4 of its 5 matches

Meaning:

The two reasonable gentle position-weighting methods produced almost the same rankings.

This suggests that the model is not highly dependent on choosing exactly `1 / sqrt(position)`.

### sqrt vs inverse position

- score correlation: 0.8639
- average Top-5 overlap: 3.46 / 5

Meaning:

`1 / position` puts much more emphasis on the first few ingredients and changes the rankings much more strongly.

## Decision

Keep `1 / sqrt(position)`.

Reject `1 / position` because it is more aggressive and produces less stable rankings.

---

# 5. Ingredient Similarity vs Formula Similarity

Ingredient Jaccard and position-weighted formula similarity were strongly related.

Earlier testing showed:

- ingredient vs raw position similarity correlation: 0.8971
- ingredient vs the tested prevalence-adjusted version: 0.9313

Meaning:

Products with high ingredient overlap usually also have high formula similarity.

Therefore, Ingredient Jaccard and Formula Similarity should not both be heavily weighted inside one composite score.

That would partly count the same ingredient information twice.

## Decision

Use:

- Ingredient Jaccard as baseline and explanation
- Formula Similarity as the main ranking signal

---

# 6. Common-Ingredient Dominance

## Problem found

The raw position-weighted similarity was strongly influenced by common moisturizer ingredients.

In the dataset:

- water appears in 50/50 products
- glycerin appears in 50/50 products
- sodium hyaluronate appears in 30/50
- phenoxyethanol appears in 28/50
- tocopherol appears in 25/50
- dimethicone appears in 24/50

Across all weighted shared-ingredient contributions:

- water contributed about 37.1%
- glycerin contributed about 21.5%

Together:

- water + glycerin contributed about 58.5%

The median product pair received about 79.8% of its shared contribution from the 10 most common ingredients.

Meaning:

Common moisturizer base ingredients influence the score strongly.

This reduces some of the model's ability to distinguish formulas.

---

# 7. Prevalence / IDF Experiment

A prevalence adjustment was tested to reduce the influence of ingredients that appear in many products.

The tested IDF formula was:

IDF(i) =
log((N + 1) / (df(i) + 1)) + 1

Two versions were tested:

1. full IDF
2. sqrt(IDF)

---

# 8. Full IDF Result

Full IDF clearly reduced common-ingredient dominance.

Water + glycerin contribution changed from:

- raw: 58.5%
- full IDF: 40.0%

Raw vs full-IDF score correlation:

- 0.9514

Average Top-5 overlap:

- 4.22 / 5

However, full IDF also strongly increased the importance of ingredients that appeared in only one or two products.

For an ingredient found in only 1/50 products:

- IDF ≈ 4.24

This could make a rare unmatched ingredient contribute more than four times its normal position weight.

## Decision

Reject full IDF.

It corrected common-ingredient dominance too aggressively.

---

# 9. sqrt(IDF) Result

A gentler version was also tested:

weight =
position weight × sqrt(IDF)

Results:

- raw vs sqrt-IDF correlation: 0.9863
- average Top-5 overlap: 4.54 / 5
- water + glycerin contribution: 58.5% → 49.4%

Meaning:

sqrt(IDF) reduced common-ingredient dominance while keeping most rankings stable.

However, one larger conceptual problem remained.

---

# 10. Why IDF Was Not Used in Formula Similarity v1

IDF depends on the products currently stored in the dataset.

For example:

An ingredient may appear in:

- 1 out of 50 products today

but later appear in:

- 100 out of 500 products

Its IDF weight would then change.

This means the similarity score between two unchanged products could change simply because unrelated products were added to the catalog.

That does not fit the core meaning of BeautyGraph's Formula Similarity.

The core Formula Similarity should mainly describe the relationship between the two formulas themselves.

## Decision

Do not use IDF or sqrt(IDF) in Formula Similarity v1.

Keep the IDF analysis as an experimental finding only.

It may be useful in the future for catalog-aware search or reranking, but not for the core pairwise formula relationship score.

---

# 11. Function Profile

Each product has a 10-dimensional function profile:

- humectant
- emollient
- occlusive
- barrier_supporting
- soothing
- antioxidant
- texture_viscosity
- preservative
- fragrance_related
- active_treatment

Each mapped ingredient contributes position weight.

If an ingredient has multiple mapped functions, its weight is divided equally across them.

Example:

If an ingredient has two functions and a position weight of 0.50:

- function 1 receives 0.25
- function 2 receives 0.25

This prevents multi-function ingredients from automatically receiving more total weight.

This equal split is a BeautyGraph normalization choice, not a chemical concentration estimate.

---

# 12. Function Similarity

Cosine similarity is used to compare the 10-dimensional function profiles.

Initial testing showed that Function Similarity contains different information from direct ingredient matching.

Across all product pairs:

- ingredient vs function correlation: 0.2021
- position vs function correlation: 0.2358

Meaning:

Function Similarity is not simply repeating the same information as ingredient overlap.

This made it a useful candidate for the project.

However, further testing found important limitations.

---

# 13. Function-Mapping Coverage Limitation

Function mapping is intentionally incomplete.

The practicum used high-impact-first mapping instead of mapping every normalized ingredient.

Product-level position-weighted function coverage:

- minimum: 33.0%
- median: 59.0%
- mean: 57.6%
- maximum: 79.2%

Meaning:

For the typical product, the current function profile represents only about 59% of the position-weighted ingredient list.

Some products have much lower coverage.

Examples:

- Bioderma SENSIBIO AR+ Cream: 33.0%
- LRP Cicaplast Balm B5+: 38.0%
- Shiseido Essential Energy: 39.8%

Low-coverage products could still receive very high cosine scores.

For example, Bioderma had only 33% weighted coverage but produced several function similarity scores above 0.90.

Correlation between pair coverage and Function Similarity:

- 0.0519

Meaning:

The cosine score does not know how much function information is missing.

This is the most important current limitation of Function Similarity.

---

# 14. Function Taxonomy Limitation

The current taxonomy contains 10 broad function groups.

This is intentionally simple and useful for explanation, but it also reduces detail.

Different ingredients may be grouped into the same broad category.

Examples include:

- many different ingredients being grouped as `emollient`
- several formulation roles being grouped under `texture_viscosity`
- different treatment-related roles being grouped as `active_treatment`

This can make formulas that use different ingredients look more similar at the function-group level.

## Decision

Do not expand the taxonomy during the practicum.

Expanding the number of function groups alone would not solve the main mapping-coverage problem and could make the profiles even more sparse.

A future version should first improve mapping coverage and then evaluate whether broad groups should be split.

---

# 15. Same-Category Limitation

All 50 frozen products are leave-on facial moisturizers or barrier creams.

Products in the same category naturally share several broad functions.

The cosine contribution analysis showed:

- emollient: 54.4%
- humectant: 23.8%
- texture_viscosity: 17.1%

Together:

- 95.3% of the cosine dot-product contribution

At the product level:

- median Top-3 function share: 79.2%
- mean Top-3 function share: 80.4%

Meaning:

Most moisturizer formulas naturally emphasize the same few broad functions.

Adding more products from the same moisturizer category would not necessarily solve this problem.

Function profiles may become more useful for discrimination if BeautyGraph later includes multiple skincare categories.

---

# 16. Final Role of Function Similarity

The function work remains useful. It answers a different question:

> What functional structure can be observed from the ingredients that have been mapped?

## Decision

Keep:

- function profile
- function similarity
- shared function analysis
- function differences

Use them for:

- Product Profile
- Compare Products
- explanations
- diagnostics

Do not use Function Similarity to control Top-5 ranking in v1.

When function similarity is shown later, mapping coverage should also be available so the score is not presented with more confidence than the data supports.

---

# 17. Composite Score Decision

An early candidate architecture was:

0.35 × ingredient similarity
+ 0.40 × position similarity
+ 0.25 × function similarity

This was not used.

## Reasons

### Ingredient and position signals overlap

They contain much of the same information.

Combining both would partly double-count ingredient similarity.

### Function data is not reliable enough for ranking

Current limitations include:

- incomplete mapping coverage
- broad taxonomy
- same-category function concentration

### The three score scales are very different

Across the 1,225 product pairs:

Ingredient similarity median:

- 0.1087

Position-weighted similarity median:

- 0.1486

Function similarity median:

- 0.8580

Meaning:

A simple weighted average would be difficult to interpret.

## Decision

Do not use the original composite score.

---

# 18. Final Similarity Architecture

Similarity Engine v1 uses three separate signals.

## `ingredient_similarity`

Plain Jaccard similarity.

Answers:

> How much normalized ingredient overlap do these products have?

Use for:

- baseline
- comparison
- explanation

---

## `formula_similarity`

Position-weighted generalized Jaccard.

Answers:

> How similar are the declared formulas when ingredient identity and ingredient rank are considered?

This is the main Similar Products ranking score.

---

## `function_similarity`

Cosine similarity of the mapped function profiles.

Answers:

> How similar are the functional patterns visible in the currently mapped ingredients?

Use for:

- explanation
- comparison
- diagnostics

It does not control Top-5 ranking.

---

# 19. Top-5 Ranking

Each product returns its five closest formula matches in the dataset.

Ranking is based only on:

`formula_similarity`

Product form remains useful context but does not directly change the formula score.

---

# 20. Domain Sanity Check

Representative products across different forms and formula styles were manually reviewed.

Examples included:

- CeraVe Moisturizing Cream
- Neutrogena Hydro Boost
- La Roche-Posay Double Repair
- Avène Balm
- COSRX Lotion
- Hada Labo Gel Cream
- Cicaplast Balm
- LRP Toleriane Fluide
- belif Aqua Bomb

No clear systematic ranking failure was found.

Some matches crossed product forms.

This was not treated as an error because product form and ingredient-formula structure are not the same thing.

## Decision

Do not add product-form as a factor in v1.

---

# 21. Final Structural Validation

The final production engine was run across the full dataset.

Results:

- products: 50
- unique product pairs: 1,225
- Top-5 rows: 250
- structural errors: 0

Validation confirmed:

- every product returns exactly 5 matches
- no self-matches
- no duplicate results
- results are correctly sorted

---

# 22. Final Formula-Similarity Distribution

## Top-1 Formula Similarity

- minimum: 0.1463
- median: 0.2689
- mean: 0.3006
- maximum: 0.7343

Meaning:

The closest match for some products is much stronger than for others.

## All Top-5 Formula Similarity Scores

- minimum: 0.0719
- median: 0.2328
- mean: 0.2396
- maximum: 0.7343

The strongest observed match was:

CeraVe Moisturizing Cream
↔
CeraVe PM Facial Moisturizing Lotion

Formula Similarity:

0.7343

---

# 23. Ranking vs Similarity Strength

A Top-5 ranking shows the closest products available in the current dataset.

It does not automatically mean that all five products have a strong formula relationship.

For example:

A product's Rank #1 result may still have a relatively low formula similarity score.

Therefore:

> Ranking and similarity strength are separate outputs.

A better UI label is:

**Closest Formula Matches**

rather than automatically describing every result as a strongly similar product.

---

# 24. Score Interpretation

Formula Similarity v1 is a mathematical comparison score.

For example:

0.70

should not currently be described as:

"70% similar"

The project has not yet created validated thresholds for labels such as:

- strong
- moderate
- weak

These labels may be evaluated later.

For now, the score is used for:

- ranking
- pair comparison
- identifying stronger and weaker formula relationships

---

# 25. Main Limitations

## Ingredient position is not concentration

The model uses ingredient-list order only as a rank signal.

## Formula details are incomplete

The model does not know:

- exact ingredient percentages
- ingredient grade
- pH
- manufacturing process
- delivery system
- final physical performance

## Common moisturizer ingredients affect the score strongly

Water, glycerin, and other common base ingredients contribute heavily to shared formula structure.

This is a known limitation of the simple v1 method.

## Function mapping is incomplete

Function profiles represent only the mapped portion of each formula.

## Function taxonomy is broad

The current 10 groups simplify many detailed ingredient roles.

## Dataset is one category

All products are moisturizers, so functional profiles naturally share many common patterns.

## Formula similarity is not product equivalence

A similar declared ingredient formula does not guarantee identical texture, performance, efficacy, or clinical effect.

BeautyGraph describes formula relationships, not chemical or clinical equivalence.

---

# 26. Final Decision

Similarity Engine v1 is complete.

The final architecture is:

Product
→ normalized ingredients
→ ingredient overlap
→ ingredient position
→ Formula Similarity
→ Top-5 closest formula matches

In parallel:

Ingredient
→ Function
→ Function Profile
→ functional comparison
→ explanation

The final ranking remains simple and transparent.

Function analysis is preserved as a separate explanation layer instead of being forced into the main ranking score.

Experimental IDF adjustments were tested and documented but are not part of production Formula Similarity v1.

---

# 27. Implementation Status

Similarity Engine v1 now supports:

- 50 frozen products
- 1,225 unique product pairs
- ingredient similarity
- formula similarity
- function similarity
- Top-5 retrieval for any product

Final automated test suite:

- 32 tests passed

Final structural validation:

- 250 Top-5 rows
- 0 errors