# Product Expansion and Function Mapping v1 Log

## 1. Product Expansion

The product expansion rules were defined before collecting new data. The scope remained limited to leave-on facial moisturizers sold in the U.S. market.

Twelve products were added to the dataset. The dataset increased from 16 to 28 products.

The new batch included:

* 4 creams
* 3 lotions
* 3 gel-creams
* 1 gel
* 1 balm

The products were selected to increase variation in product form, brand, price, and formula structure. The batch was intended to test the BeautyGraph pipeline, not to represent the full moisturizer market.

The original source text and ingredient order were preserved. No new product fields, claims fields, archetype fields, or extra worksheets were added.

## 2. Pipeline Results

The updated workbook passed the data inspection checks:

* 28 product rows
* no duplicate product IDs
* no missing required fields

The full pipeline successfully processed the expanded dataset:

* 28 products ingested
* 913 ingredient records parsed
* 913 ingredient records normalized

All 28 products produced valid ingredient records with continuous ingredient positions.

## 3. Parser Review

The new product data did not expose any parser errors.

The parser correctly handled:

* comma-separated ingredient lists
* line breaks and bullet separators
* numeric commas such as `1,2-Hexanediol`
* slash and backslash ingredient names
* multilingual ingredient labels
* ingredient names containing parentheses

No parser code changes were needed. The parser remains at version `v1`.

## 4. Normalization Updates

The expanded data exposed several ingredient-name variants that needed to be combined.

The first update fixed:

* a misspelled ingredient name
* a bilingual ingredient label
* an additional fragrance label format

This update was released as normalizer `v2`.

A later review found more common-name and multilingual variants, including different forms of shea butter, mineral oil, microcrystalline wax, sunflower seed oil, soybean oil, and several plant extracts.

These variants were added as explicit aliases and released as normalizer `v3`.

All changes were added test-first. The final test result was:

* 16 tests passed

After running normalizer `v3`, the database contained:

* 913 ingredient records
* 390 unique normalized ingredients

## 5. Function Mapping v1 Rules

Function Mapping v1 was created to support the BeautyGraph prototype. It was not intended to classify every ingredient in the database.

The candidate pool included:

1. the top 100 ingredients ranked by frequency and formula position; and
2. every ingredient appearing within the first 10 positions of at least one product.

After normalization cleanup, the final review pool contained 170 unique ingredients.

Each candidate was assigned one of three statuses:

* `mapped`: the ingredient had enough support for one or more current function groups;
* `taxonomy_gap`: the ingredient had a known function that was not represented by the current taxonomy;
* `deferred_evidence`: the available evidence was not strong or specific enough for a reliable mapping.

An unmapped ingredient was not treated as having no function. It only meant that the ingredient was not classified in Function Mapping v1.

Most direct mappings were based on the functions listed in COSMILE Europe. COSMILE states that its ingredient-function information comes from the European Commission’s CosIng database.

Published papers were used when a project function such as `barrier_supporting`, `soothing`, `occlusive`, `antioxidant`, or `active_treatment` could not be supported by a direct CosIng or COSMILE function label.

## 6. Function Mapping v1 Results

The final review contained:

* 136 mapped ingredients
* 21 taxonomy-gap ingredients
* 13 deferred-evidence ingredients

The final mapping file contained:

* 165 ingredient-function relationships
* 136 unique mapped ingredients
* all 10 BeautyGraph function groups represented

The mapping was loaded into the database with:

```text
mapping_version = v1
```

The database loader matches mappings by `normalized_name` and then resolves the current database `ingredient_id`. This allows the mappings to be reloaded after ingredient IDs are rebuilt.

## 7. Coverage Results

Function Mapping v1 covered:

* 534 of 913 total ingredient records: 58.5%
* 223 of 280 top-10 ingredient records: 79.6%
* 60% to 90% of the top 10 ingredients for each individual product

The top-10 coverage result was used as the main check because it better represents the main structure of each formula.

The lower total-record coverage was accepted because many unmapped records were low-position ingredients, solvents, pH adjusters, emulsifiers, formulation-support ingredients, or uncommon extracts.

Water accounted for 25 unmapped top-10 records. It was not placed in `humectant` because its main formula role is usually solvent, and the project does not currently have a solvent group.

## 8. Taxonomy Decision

The existing 10 function groups were kept for Function Mapping v1:

* humectant
* emollient
* occlusive
* barrier_supporting
* soothing
* antioxidant
* texture_viscosity
* preservative
* fragrance_related
* active_treatment

No solvent, buffering, chelating, surfactant, or emulsifier groups were added.

These functions are common in formulations, but they currently provide limited value for the project’s consumer-facing moisturizer comparison. Adding them could also increase similarity scores mainly because products share common formulation-support ingredients.

The taxonomy can be expanded later if unmapped ingredients cause clear problems in product explanations or similarity results. Any changes made after Function Mapping v1 is used will be released under a new mapping version.

## 9. Final State

At the end of this work, BeautyGraph contained:

* 28 moisturizer products
* 913 product-ingredient records
* 390 unique normalized ingredients
* parser version `v1`
* normalizer version `v3`
* function mapping version `v1`
* 165 function mappings
* 136 mapped ingredients

The data is ready for the next stage:

* ingredient-overlap similarity
* position-weighted ingredient similarity
* function-group similarity
* similarity result review and evaluation

## References

1. European Commission. **Cosmetic Ingredient Database — CosIng.** Used as the official source for cosmetic ingredient names and listed cosmetic functions. Accessed August 2026.

2. COSMILE Europe. **Cosmetic Ingredient Database.** Used as the main searchable source for ingredient functions and ingredient descriptions. COSMILE states that its function information is sourced from CosIng. Accessed August 2026.

3. Schild J, Kalvodová A, Zbytovská J, Farwick M, Pyko C. **The role of ceramides in skin barrier function and the importance of their correct formulation for skincare applications.** International Journal of Cosmetic Science. 2024;46(4):526–543. PMID: 39113291. Used for ceramides and related skin-barrier lipids.

4. Bravo B, Correia P, Gonçalves Junior JE, Sant’Anna B, Kerob D. **Benefits of topical hyaluronic acid for skin quality and signs of skin aging: From literature review to clinical evidence.** Dermatologic Therapy. 2022;35(12):e15903. PMID: 36200921. Used for hyaluronic acid and related ingredients.

5. Ong RR, Goh CF. **Niacinamide: a review on dermal delivery strategies and clinical evidence.** Drug Delivery and Translational Research. 2024;14(12):3512–3548. PMID: 38722460. Used for niacinamide.

6. Proksch E, de Bony R, Trapp S, Boudon S. **Topical use of dexpanthenol: a 70th anniversary article.** Journal of Dermatological Treatment. 2017;28(8):766–773. PMID: 28503966. Used for panthenol.

7. Ghadially R, Halkier-Sorensen L, Elias PM. **Effects of petrolatum on stratum corneum structure and function.** Journal of the American Academy of Dermatology. 1992;26(3 Pt 2):387–396. PMID: 1564142. Used for petrolatum and mineral-oil occlusive mapping.

8. Katiyar SK, Elmets CA. **Green tea polyphenolic antioxidants and skin photoprotection.** International Journal of Oncology. 2001;18(6):1307–1313. PMID: 11351267. Used for green tea extract.

9. Gorouhi F, Maibach HI. **Role of topical peptides in preventing or treating aged skin.** International Journal of Cosmetic Science. 2009;31(5):327–345. PMID: 19570099. Used for peptide ingredients.

10. Kurtz ES, Wallo W. **Colloidal oatmeal: history, chemistry and clinical properties.** Journal of Drugs in Dermatology. 2007;6(2):167–170. PMID: 17373175. Used for oat-derived soothing and skin-protecting functions.

The exact source used for each individual ingredient-function relationship is also stored in the `source` column of `ingredient_function_map.csv`.
