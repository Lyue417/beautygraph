# BeautyGraph Product Expansion Rules

## Purpose

These rules define how products are selected and recorded for the BeautyGraph facial moisturizer dataset. The dataset is designed to support ingredient parsing, normalization, ingredient-function mapping, and explainable formula similarity. 

## 1. Product Scope

A product may be included only if it is a leave-on facial moisturizer marketed for routine facial use.

Included product forms:

* `cream`
* `lotion`
* `gel`
* `gel_cream`
* `balm`
* `fluid`
* `milk`
* `ointment`

Excluded products:

* sunscreens or moisturizers with SPF;
* cleansers, serums, essences, toners, masks, and facial oils;
* eye creams;
* body-only moisturizers;
* prescription or medicated products;
* tinted complexion products;
* products without a complete and traceable ingredient list.

## 2. Unit of Record

One row represents one distinct product formula in one market.

Different package sizes of the same formula are not separate products.

A reformulated product or a product with a materially different regional ingredient list must be treated as a separate formula version or excluded when the version cannot be determined.

## 3. Market

The current dataset focuses on products available in the United States.

The ingredient list, product name, size, and price should refer to the same market version whenever possible.

## 4. Source Priority

Sources are selected in this order:

1. Current official United States brand product page.
2. Authorized United States retailer, such as Sephora, Ulta, Target, or a comparable retailer, when the official page does not provide a complete ingredient list.
3. Official international brand page only when the formula can be verified as the same version sold in the United States.

Crowdsourced databases, marketplace sellers, blogs, ingredient-analysis websites, and review pages are not used as the canonical source for this collection batch.

## 5. Source Conflicts

Do not combine fields from conflicting product versions into one synthetic record.

When sources disagree:

* select one canonical source;
* preserve its ingredient list exactly;
* record the conflict in `data_notes`;
* do not manually reconcile two different ingredient lists;
* exclude the product when the market or formula version cannot be determined.

## 6. Required Data

Each included product must have:

* a stable product ID;
* product and brand names;
* category and product form;
* source name, type, URL, and access date;
* a complete raw ingredient list.

Price and size should be recorded when available from the same canonical source. Missing non-core commercial fields must be documented in `data_notes`.

## 7. Raw and Normalized Fields

`product_name_raw`, `brand_raw`, and `raw_ingredient_list` preserve source information.

Normalized product and brand names may standardize capitalization, trademark symbols, and whitespace, but must not shorten or reinterpret the product identity.

The ingredient list must not be manually normalized before ingestion.

## 8. Product Form

`product_form` records observable physical form, not product claims or formula archetypes.

Examples:

* “gel moisturizer” → `gel`
* “gel cream” or “water gel cream” → `gel_cream`
* “facial lotion” → `lotion`
* “recovery balm” → `balm`
* “rich moisturizer” without another explicit form → `cream`

Claims such as barrier repair, soothing, sensitive skin, anti-aging, or peptide are not product forms.

## 9. Batch Coverage

Each expansion batch should improve product-form, brand, price, and formula diversity.

For the next batch:

* no more than half of the products should be creams;
* include at least three gel or gel-cream products;
* include at least two lotions;
* include at least one balm or another currently underrepresented form;
* include affordable, mid-range, and premium products;
* include both established and newer brands;
* include products likely to introduce different ingredient structures.

Product-form and source quality take priority over brand prestige or price balance.

## 10. Collection Boundary

Only the existing 18 product fields are collected.

The current expansion does not add:

* product claims;
* reviews;
* formula archetypes;
* multiple retailer offers;
* price history.

## 11. Batch Acceptance Criteria

A batch is accepted only when:

* all product IDs are unique;
* all products meet the category scope;
* every product has a complete ingredient list;
* source URLs and access dates are present;
* product forms use the controlled vocabulary;
* source or version conflicts are documented;
* the workbook passes the existing inspection script;
* the complete ingest, parse, normalize, and audit pipeline succeeds.
