# BeautyGraph Ingredient Function Taxonomy

## Purpose

This taxonomy defines the controlled ingredient-function categories used in the BeautyGraph practicum prototype.

The taxonomy is designed specifically for comparing leave-on facial moisturizers. It is not intended to be a complete cosmetic ingredient classification system or a clinical classification of ingredient efficacy.

Ingredient-function mappings support the BeautyGraph Product → Ingredient → Function data model, formula function profiles, product comparison, and function-similarity analysis.

## Function Categories

| Function | Definition | Example Ingredients |
|---|---|---|
| `humectant` | Ingredients primarily used to attract or retain water and support hydration. | glycerin, sodium hyaluronate, sodium PCA |
| `emollient` | Ingredients that soften or smooth the skin surface and contribute to the lipid or slip characteristics of a formula. | squalane, dimethicone, cetearyl alcohol |
| `occlusive` | Ingredients that help reduce water loss by forming or contributing to a relatively water-resistant surface layer. | shea butter, petrolatum-type materials where mapped |
| `barrier_supporting` | Ingredients mapped to support the structure, maintenance, or recovery of the skin barrier. | ceramides, cholesterol, panthenol |
| `soothing` | Ingredients mapped to calming or irritation-reducing roles relevant to moisturizer comparison. | panthenol and other mapped soothing ingredients |
| `antioxidant` | Ingredients used for antioxidant activity in the formula or on the skin. | tocopherol, hydroxyacetophenone |
| `texture_viscosity` | Ingredients that materially contribute to formula texture, viscosity, thickening, or related physical properties. | carbomer, xanthan gum, cetearyl alcohol |
| `preservative` | Ingredients used primarily to help protect the product from microbial spoilage. | phenoxyethanol, sodium benzoate, chlorphenesin |
| `fragrance_related` | Ingredients whose mapped role is fragrance or fragrance-related sensory contribution. | fragrance |
| `active_treatment` | Treatment-oriented cosmetic ingredients whose role goes beyond basic moisturization in the context of the prototype. | niacinamide and other mapped treatment-oriented ingredients |

## Mapping Rules

### Many-to-Many Mapping

An ingredient may belong to more than one function category when supported by the available evidence.

For example:

- glycerin → `humectant`, `texture_viscosity`
- cetearyl alcohol → `emollient`, `texture_viscosity`
- panthenol → `humectant`, `barrier_supporting`, `soothing`
- niacinamide → `barrier_supporting`, `active_treatment`

BeautyGraph therefore treats the Ingredient → Function relationship as many-to-many rather than assigning every ingredient to a single category.

### Evidence and Confidence

Ingredient-function mappings are maintained separately from the taxonomy itself.

Mappings may use cosmetic ingredient references such as COSMILE Europe and ingredient-specific scientific literature. Each mapping can include a source, confidence level, and notes.

The taxonomy category is controlled by BeautyGraph, while the evidence supports whether a specific ingredient should be mapped to that category.

### Unmapped Ingredients

Not every normalized ingredient is required to receive a function mapping.

An ingredient may remain unmapped when:

- evidence is insufficient for a confident project-level mapping;
- its primary role is outside the current taxonomy;
- the ingredient has little impact on the current moisturizer-comparison use case.

Examples of roles not modeled as separate categories in this prototype include some solvents, emulsifiers, chelating agents, and pH adjusters.

This is intentional. BeautyGraph prioritizes reliable mappings that materially support moisturizer comparison rather than forcing complete coverage.

## Use in Formula Profiles

For mapped ingredients, BeautyGraph uses ingredient position to construct product-level function profiles.

When an ingredient has multiple mapped functions, its contribution is distributed across those functions rather than counted at full weight in every category. This avoids artificially increasing the total contribution of multi-function ingredients.

The resulting function profile is used as a supporting comparison signal and explanation layer.

## Scope and Limitations

This taxonomy is:

- scoped to the current leave-on facial moisturizer dataset;
- designed for information organization and formula comparison;
- intentionally broad and interpretable;
- not a complete representation of cosmetic formulation science;
- not intended to establish clinical efficacy, safety, or treatment claims.

Some broad categories, especially `humectant`, `emollient`, and `texture_viscosity`, cover many commonly occurring moisturizer ingredients. Function similarity is therefore treated as a supporting signal rather than the primary ranking method for similar products.

Future versions of BeautyGraph may extend or refine the taxonomy if additional product categories or use cases require more specific functional distinctions.
