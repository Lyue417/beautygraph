# Dataset Scope

## Project Scope

The final BeautyGraph practicum dataset contains 50 skincare products.

The dataset focuses on leave-on facial moisturizers and barrier creams that are available in the U.S. market. It is designed to support formula comparison, ingredient-function analysis, and explainable product similarity.


## Sampling Approach

Products were selected using a bounded purposive sampling approach.

Selection priorities were:

1. U.S. market availability and visibility
2. Reliable ingredient-list sources
3. Formula and product-form diversity
4. Price and brand diversity
5. Geographic diversity

The dataset was not balanced by country, price tier, or product form. These factors were used to improve coverage and formula diversity rather than to create representative quotas.

## Final Dataset

Final product count: 50

Product forms:

- cream: 23
- gel_cream: 10
- lotion: 6
- balm: 3
- fluid: 3
- gel: 3
- milk: 2

All products belong to the moisturizer category.

## Data Sources

Ingredient lists were collected primarily from official brand websites. Authorized retailer sources were used when necessary.

The dataset records:

- product and brand names
- product form
- source information
- ingredient list
- regular listed price
- size
- price per unit

Temporary sale prices, subscription discounts, coupons, and sitewide promotions were not used as the standard product price.

Price is stored as contextual product information and is not used as an input to formula similarity.

## Ingredient Processing

The final dataset contains:

- 50 products
- 1,532 ordered product-ingredient records
- 555 unique normalized ingredients

Ingredient lists were parsed while preserving ingredient order.

Normalization uses conservative explicit aliases for confirmed equivalent names and spelling variants. Distinct ingredient forms are kept separate unless equivalence can be confirmed.

## Ingredient Function Mapping

Ingredient functions are mapped to the following taxonomy:

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

Function Mapping v2 contains 187 ingredient-function relationships for 154 ingredients.

Final mapping coverage:

- all ingredient records: 54.9%
- first 10 ingredient positions: 73.8%

Unmapped ingredients are retained when available evidence is insufficient or when their primary role falls outside the current taxonomy, such as solvents, emulsifiers, chelating agents, or pH adjusters.

## Limitations

Ingredient order is used only as an approximate indicator of formula prominence and does not provide exact ingredient concentrations.

Ingredient lists do not capture formulation details such as concentration, manufacturing process, pH, stability, delivery systems, or clinical performance.

Ingredient-function classifications are simplified project-level categories and may depend on formulation context.

Formula similarity should not be interpreted as product equivalence or equal efficacy.

Function-profile completeness varies across products because the project taxonomy intentionally does not cover every formulation role.

## Data Freeze

The practicum dataset is frozen at 50 products.

Further product expansion and taxonomy expansion are outside the practicum implementation scope unless a clear data error is discovered.