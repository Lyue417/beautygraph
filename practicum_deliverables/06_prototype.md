# BeautyGraph Prototype

## 1. Purpose

This deliverable documents the final BeautyGraph prototype and points to the canonical implementation.

BeautyGraph is a lightweight, explainable skincare formula-comparison prototype built around a dataset of 50 leave-on facial moisturizers.

The prototype is designed to help users:

- understand one product's ingredient structure;
- find similar formulas;
- compare two formulas;
- and see the ingredient and function evidence behind the similarity results.

The public prototype is available at:

**https://lyue417.github.io/beautygraph/**

---

## 2. Final Prototype Files

The final public prototype is implemented as a static website.

Canonical files:

```text
docs/index.html
docs/beautygraph_data.json
docs/assets/
```

Archived prototype versions:

```text
docs/prototype_v1.html
docs/prototype_v2.html
```

`docs/index.html` is the current public version.

`docs/prototype_v1.html` preserves the version used before the usability-driven redesign.

`docs/prototype_v2.html` preserves the revised version created after the evaluation findings were incorporated.

The public site is hosted through GitHub Pages.

---

## 3. Why the Public Prototype Is Static

The data-processing pipeline uses Python and PostgreSQL, but the public prototype does not require a live database.

The project pipeline produces a frozen serving dataset:

```text
docs/beautygraph_data.json
```

The browser interface reads this exported dataset directly.

This architecture keeps the demo:

- lightweight;
- easy to share;
- reproducible;
- independent of a running local database;
- and appropriate for a practicum prototype.

The underlying processing pipeline remains separate from the serving interface.

---

## 4. Main User Flow

The final prototype uses the navigation order:

```text
Product Profile
→ Similar Products
→ Compare Products
→ About
```

This reflects the intended exploration flow:

1. understand one product;
2. discover similar formulas;
3. choose a result for deeper comparison;
4. review project scope and limitations.

---

## 5. Product Profile

The Product Profile page helps users understand one formula.

A user selects a moisturizer and sees:

- brand and product name;
- product form;
- ingredient count;
- Function Coverage;
- Formula Function Profile;
- plain-language function-group descriptions;
- ingredients mapped to each function group;
- expandable ingredient lists within function groups;
- the full ingredient list in published order.

### Function Profile

The Function Profile shows the distribution of mapped ingredient-role contributions across the controlled function groups.

The visible percentages add up to 100% of the mapped Function Profile.

They are not ingredient concentration percentages.

### Function Coverage

Function Coverage explains how much of the position-weighted ingredient-list structure currently has ingredient-function mappings.

Ingredients outside the mapped portion:

- remain visible in the ingredient list;
- still contribute to Ingredient Overlap;
- still contribute to Formula Similarity;
- but do not contribute to the Function Profile or Function Similarity.

---

## 6. Similar Products

The Similar Products page allows a user to select one product and view its five closest formula matches in the current BeautyGraph dataset.

The results are ranked by:

**Formula Similarity**

The page also displays:

- Ingredient Overlap;
- Function Similarity;
- number of shared ingredients;
- shared high-position ingredients;
- expandable evidence when more shared high-position ingredients are available;
- and a direct action to compare the selected product with a recommended match.

### Ranking logic

Formula Similarity is the ranking score.

It considers:

- which normalized ingredients are shared;
- and where those ingredients appear in each published ingredient list.

Ingredients appearing earlier in both lists receive more influence.

Ingredient Overlap and Function Similarity are supporting signals and do not determine the Top-5 order.

---

## 7. Compare Products

The Compare Products page allows a user to select any two products in the dataset.

The page shows three separate similarity questions.

### Formula Similarity

**Question:** Do important parts of the ingredient structures line up?

This is the position-weighted ranking score.

### Ingredient Overlap

**Question:** How many exact normalized ingredients do the products share?

This is based on ingredient-set overlap without ingredient position.

### Function Similarity

**Question:** Do the mapped ingredients play similar overall roles?

This compares the mapped function patterns.

The three scores are intentionally shown separately because they answer different questions.

For example, two products can have low Ingredient Overlap but high Function Similarity when different ingredients perform similar roles.

---

## 8. Comparison Evidence

The comparison page provides additional evidence instead of presenting the scores alone.

### Shared ingredients

The interface shows:

- total shared normalized ingredients;
- shared ingredients appearing within the first 10 positions of both lists;
- expandable access to all shared ingredients.

### Function-profile comparison

Each function group is shown with aligned Product A and Product B bars.

Users can expand a function group to see which mapped ingredients in each product contribute to that group.

This makes it possible to see that a function group can be:

- present in both products;
- similar in role;
- but different in relative profile share.

### Product-specific ingredients

The interface also shows ingredients found only in Product A and ingredients found only in Product B.

---

## 9. Homepage Explanation Layer

Prototype v2 added a homepage explanation layer because the usability walkthrough showed that users could complete tasks but did not always understand the technical metrics.

The homepage now explains:

```text
Ingredient list
→ standardized ingredient names
→ ingredient roles
→ function groups
→ formula comparison
```

It also provides plain-language definitions of the controlled function groups and explains the three similarity scores as three different questions.

The goal is to reduce the amount of interpretation users must perform on their own.

---

## 10. Prototype v1

Prototype v1 established the complete end-to-end system:

```text
Product
→ Ingredient
→ Function
→ Similarity
→ Explanation
→ User Interface
```

It included:

- Product Profile;
- Compare Products;
- Similar Products;
- percentage-based similarity signals;
- formula-function profiles;
- deterministic comparison explanations.

Prototype v1 is archived at:

```text
docs/prototype_v1.html
```

It is also preserved in the Git history under the `prototype-v1` tag.

---

## 11. Prototype v1 Evaluation Findings

The v1 usability walkthrough showed that the main problem was not task completion.

All three participants completed all three core tasks.

The main problems were interpretation and terminology.

Examples included confusion about:

- Function Coverage;
- Formula Similarity;
- Ingredient Overlap;
- Function Similarity;
- why ingredient similarity could be low while function similarity was high;
- whether Function Profile percentages represented ingredient concentrations;
- what technical terms such as normalized ingredients or mapped function profile meant.

Participants also wanted clearer connections between function groups and the ingredients that produced those function signals.

These findings are documented in:

```text
07_evaluation_summary.md
```

---

## 12. Prototype v2

Prototype v2 was created in response to the v1 evaluation.

Major changes included:

- adding homepage onboarding;
- explaining the Product → Ingredient → Function → Comparison logic;
- adding plain-language function-group definitions;
- clearly separating the three similarity metrics;
- identifying Formula Similarity as the ranking score;
- replacing ambiguous `DATA COVERAGE` language with Function Coverage;
- clarifying that Function Profile percentages are not concentrations;
- ensuring displayed Function Profile percentages sum to 100%;
- connecting function groups directly to mapped ingredients;
- adding expandable ingredient evidence;
- replacing narrative-heavy function comparison with aligned visual bars;
- adding a direct Similar Products → Compare Products action;
- simplifying technical user-facing language;
- changing navigation to Product Profile → Similar Products → Compare Products → About.

Prototype v2 is archived at:

```text
docs/prototype_v2.html
```

It is also preserved in the Git history under the `prototype-v2` tag.

---

## 13. Responsive Interface

The public prototype is designed to work at different browser widths.

Responsive behavior includes:

- multi-column layouts collapsing to single-column layouts;
- smaller product-summary cards in Compare Products;
- wrapped ingredient chips;
- expandable ingredient lists instead of permanently displaying very long lists;
- responsive function-profile and comparison layouts.

The final prototype was smoke-tested at desktop and narrow browser widths.

---

## 14. Visual Design

The prototype uses a lightweight editorial visual style with:

- soft neutral backgrounds;
- sage green accents;
- large serif headings;
- simple rounded cards;
- generic watercolor product-form illustrations.

The illustrations represent product form rather than actual commercial product packaging.

Product-form illustrations include categories such as:

- cream;
- gel cream;
- lotion;
- balm;
- fluid;
- gel;
- milk.

The visual layer is intended to support readability and prototype communication rather than reproduce exact packaging.

---

## 15. Technology

The final prototype uses:

```text
HTML
CSS
JavaScript
JSON
GitHub Pages
```

The broader BeautyGraph project uses:

```text
Python
PostgreSQL
SQLAlchemy
pytest
```

Streamlit was used during earlier local prototype development, while the final shareable public demo uses a static HTML/CSS/JavaScript interface.

---

## 16. Deployment

The public demo is hosted through GitHub Pages:

**https://lyue417.github.io/beautygraph/**

The deployed page reads the frozen serving dataset from:

```text
docs/beautygraph_data.json
```

This allows reviewers to use the prototype without installing Python, PostgreSQL, or project dependencies.

---

## 17. Prototype Scope

The prototype contains:

- 50 leave-on facial moisturizers;
- multiple moisturizer forms;
- normalized ingredient data;
- controlled ingredient-function mappings;
- all pairwise product similarity results;
- Top-5 recommendations;
- formula-function profiles;
- ingredient-level comparison evidence.

It is a scoped proof of concept rather than a complete skincare search engine.

---

## 18. Limitations

The prototype compares structured published ingredient-list information.

It does not establish identical:

- ingredient concentrations;
- formulation;
- texture;
- stability;
- performance;
- clinical efficacy;
- safety;
- medical suitability.

Ingredient-list order is used as an approximation of formula structure.

Function-based results are limited by current ingredient-function mapping coverage.

The prototype currently contains only one product category and should not be interpreted as representing the full skincare market.

---

## 19. Evaluation Status

Prototype v1 received the formal lightweight user walkthrough documented in the project evaluation.

Prototype v2 was redesigned in response to those findings and was checked through functional and layout smoke testing.

A second formal participant study of Prototype v2 was not completed.

---

## 20. Canonical Artifact

This document serves as the review-friendly index for the prototype deliverable.

The canonical working artifact is:

```text
docs/index.html
```

with serving data in:

```text
docs/beautygraph_data.json
```

and the public demo at:

**https://lyue417.github.io/beautygraph/**

The archived versions preserve the design iteration:

```text
Prototype v1
→ usability evaluation
→ Prototype v2
```

This iteration is part of the final practicum works, not a separate product-development track.
