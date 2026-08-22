# BeautyGraph Evaluation Summary

## 1. Purpose

The evaluation focused on two questions:

1. Does the baseline similarity system return formula matches that are generally reasonable?
2. Can users understand and use the three core prototype functions: Product Profile, Similar Products, and Compare Products?

---

## 2. Manual Similarity Review

### Method

A manual review was completed for the Top-5 similarity results of 10 query products selected from different product forms in the 50-product dataset.

This produced:

- 10 query products
- 5 ranked matches per query
- 50 reviewed product pairs

Each match was labeled as:

- `Reasonable`
- `Questionable / weak`

The review considered:

- number of shared normalized ingredients,
- shared ingredients appearing relatively early in both ingredient lists,
- overall formula structure,
- mapped function-profile similarity,
- and whether the recommendation was understandable from the available formula evidence.

The full review records are stored in:

`data/evaluation/manual_similarity_review.csv`

### Results

| Result | Count | Share |
|---|---:|---:|
| Reasonable | 36 | 72% |
| Questionable / weak | 14 | 28% |
| Total | 50 | 100% |

Results were stronger at the top of the ranking:

| Rank | Reasonable | Questionable / weak |
|---|---:|---:|
| 1 | 10 | 0 |
| 2 | 10 | 0 |
| 3 | 8 | 2 |
| 4 | 5 | 5 |
| 5 | 3 | 7 |

All Rank-1 and Rank-2 recommendations in the reviewed sample were judged reasonable.

Lower-ranked results were more mixed. Weak matches often shared common moisturizer ingredients such as water, glycerin, or dimethicone but had more substantial differences in the rest of the high-position formula structure.

### Interpretation

The manual review supports using the current position-weighted Formula Similarity as a reasonable baseline ranking method for the prototype.

The results also show an important limitation: Function Similarity alone should not be used as the ranking score. Two products can have very similar mapped function profiles while using substantially different ingredient structures.

The current design therefore uses Formula Similarity for ranking and presents Ingredient Overlap and Function Similarity as supporting explanatory signals.

This is a baseline validation rather than evidence that the ranking is objectively optimal. The manual judgments are subjective and the reviewed sample covers only 50 product-pair recommendations.

---

## 3. User Walkthrough

### Method

Three participants completed a lightweight walkthrough of Prototype v1.

Each participant was asked to use:

1. Product Profile
2. Compare Products
3. Similar Products

This produced:

- 3 participants
- 3 tasks per participant
- 9 task attempts

The detailed walkthrough records are stored in:

`data/evaluation/user_walkthrough.csv`

### Task Completion

All participants completed all three tasks.

| Task | Completed |
|---|---:|
| Product Profile | 3 / 3 |
| Compare Products | 3 / 3 |
| Similar Products | 3 / 3 |
| Total | 9 / 9 |

The main usability problem was interpretation.

---

## 4. Main Usability Findings

### 4.1 Similarity metrics were difficult to interpret

Participants did not always understand the difference between:

- Ingredient Overlap,
- Formula Similarity,
- and Function Similarity.

A particularly confusing case was when two formulas had low ingredient and formula similarity but high function similarity.

Users needed a direct explanation that different ingredients can perform similar roles, so two formulas can have different ingredient structures while still having similar function profiles.

Users also needed to understand that Formula Similarity is the score used to rank Similar Products.

### 4.2 Function Profile percentages could be misinterpreted

Function Profile percentages were not immediately understandable.

One participant could interpret the percentages as ingredient concentration percentages.

The intended meaning is different: the Function Profile summarizes the relative distribution of mapped ingredient-function contributions after ingredient-list position is considered.

The displayed function groups make up 100% of the mapped Function Profile, not 100% of the physical ingredient concentrations.

### 4.3 Function coverage needed a clearer explanation

The Prototype v1 label such as `67% DATA COVERAGE` did not explain:

- what was covered,
- why the value was below 100%,
- or how it related to the Function Profile.

Users needed to understand that function coverage represents the portion of the position-weighted ingredient-list signal for which BeautyGraph currently has function mappings.

Ingredients outside this mapped portion are still part of the ingredient list and still contribute to ingredient-based similarity.

### 4.4 Technical terminology created unnecessary difficulty

Terms such as:

- normalized ingredients,
- mapped function profile,
- function pattern,
- and largest profile differences

reflected the internal data model but were not always useful as user-facing language.

Participants generally wanted the system to translate the data into conclusions rather than requiring them to interpret technical terms themselves.

### 4.5 Ingredient-to-function relationships were useful when made visible

Users wanted to know which ingredients contributed to each function group.

Showing only a percentage for a group such as Humectant or Emollient was less useful than showing both:

- what the group means,
- and which ingredients in the selected product contribute to that group.

### 4.6 Similar Products was the easiest core function to understand

Participants responded positively to:

- the Top-5 ranking,
- percentage scores,
- and descending result order.

This interaction pattern was retained in Prototype v2.

---

## 5. Prototype v1 to Prototype v2 Changes

The usability findings were used to revise the prototype.

| Prototype v1 finding | Prototype v2 response |
|---|---|
| Users lacked a mental model for how BeautyGraph works | Added homepage onboarding explaining the chain from ingredient list → standardized ingredient → ingredient role → function group → formula comparison |
| Function groups were unfamiliar | Added plain-language definitions of the 10 function groups |
| Similarity metrics were confusing | Explained the three metrics as three different questions and identified Formula Similarity as the ranking score |
| Low ingredient similarity with high function similarity was confusing | Added direct plain-language explanations that different ingredients can perform similar roles |
| Function percentages could be mistaken for concentrations | Explicitly explained that Function Profile percentages describe the mapped functional pattern, not ingredient concentrations |
| Function Profile display percentages did not visually total 100% because of independent rounding | Updated display rounding so the visible Function Profile percentages sum to 100% |
| Function coverage was unclear | Replaced the ambiguous `DATA COVERAGE` presentation with a direct Function Coverage explanation |
| Users wanted to see which ingredients support each function group | Added ingredient chips under each function group, with expandable full lists |
| Compare Products relied too heavily on narrative explanation | Added aligned Product A / Product B function-profile bars and expandable ingredient evidence |
| Similar Products score meanings were unclear | Made Formula Similarity the clearly labeled ranking score and presented Ingredient Overlap and Function Similarity as supporting signals |
| Users wanted an easier path from similar-product discovery to detailed comparison | Added a direct `Compare these products` action |
| Similar Products was useful and easy to understand | Preserved the Top-5 descending ranking structure |
| Navigation did not match the preferred exploration flow | Changed navigation to Product Profile → Similar Products → Compare Products → About |
| Ingredient-list position numbers added visual clutter | Removed numeric labels from ingredient chips while preserving published ingredient order |

Prototype v1 remains archived as:

`docs/prototype_v1.html`

Prototype v2 is the usability-driven revision of the prototype.

---

## 6. What the Evaluation Supports

The evaluation provides evidence that:

- the baseline similarity ranking produces reasonable high-ranked matches in the reviewed sample;
- the three core prototype tasks can be completed;
- the Top-5 Similar Products interaction is understandable and useful;
- and explainability requires more than exposing model outputs or technical terminology.

A major design lesson was that users should not be expected to translate similarity scores and data-model concepts into conclusions on their own.

The prototype therefore evolved from primarily displaying structured data toward explaining:

- what a metric represents,
- why two products received a particular relationship,
- and what ingredient-level evidence supports that relationship.

---

## 7. Limitations

This evaluation has several limitations.

### Small usability sample

Only three participants completed the walkthrough. The results are useful for identifying obvious comprehension and presentation problems but are not a broad usability study.

### Manual similarity judgments

The similarity review was based on human inspection rather than an external ground-truth similarity dataset.

The `Reasonable` and `Questionable / weak` labels should therefore be treated as a sanity check of the baseline model rather than an objective accuracy measure.

### Limited product scope

The prototype contains 50 leave-on facial moisturizers. Findings should not automatically be generalized to other skincare categories.

### Partial function mapping

Not every ingredient has a mapped function. Function Profile and Function Similarity therefore use only the mapped portion of each formula.

### Ingredient-list limitations

Published ingredient order provides useful approximate structural information but does not reveal exact concentrations.

### No clinical or performance validation

BeautyGraph evaluates structured ingredient-list relationships.

Similarity scores do not establish identical:

- formulation,
- concentration,
- texture,
- stability,
- safety,
- clinical performance,
- or suitability for a specific user.

### Prototype v2 was not formally re-tested

Prototype v2 was designed in response to the Prototype v1 walkthrough findings and was checked for functionality and layout.

A second formal participant walkthrough of Prototype v2 was not conducted.

---

## 8. Conclusion

The evaluation suggests that BeautyGraph works best when similarity results are paired with clear, ingredient-level explanations.

The baseline Formula Similarity ranking performed well for the highest-ranked recommendations in the reviewed sample, while the user walkthrough showed that the major challenge was making the underlying relationships understandable.

Prototype v2 therefore focuses on translating the existing data model into clearer user-facing explanations without changing the core similarity engine.
