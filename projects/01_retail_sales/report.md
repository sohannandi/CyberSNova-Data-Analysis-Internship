# Project 1 — Retail Sales Performance Analysis

**Level:** Beginner  
**Intern:** Sohan Nandi  
**Domain:** Data Analysis  
**Registration number:** CSN-OC-2026-474  
**Internship month/year:** October 2026  

## Dataset filename and source/attribution
- **File:** `Dataset/Sample - Superstore.csv`
- **Source:** Provided by the internship; a sample Superstore retail dataset containing order-line records with sales, profit, quantity, discount, category, segment, region, state, and shipping mode fields.

## Business objective and questions
Analyze retail sales and profit from the Superstore dataset to answer:
- Which regions, states, categories, and sub-categories generate the most sales and profit?
- Which products, customer segments, or regions have low or negative profit?
- How do sales and profit vary over time?
- How do discounts relate to profitability?
- What are the shipping and order trends?

## Dataset profile
- **Rows:** 9994 order-line records
- **Columns:** 21 (Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit)
- **Data types:** All numeric fields (Sales, Quantity, Discount, Profit) are float/int; date fields parsed as datetime; categorical fields are strings.
- **Descriptive statistics:** Total sales $2,297,200.86 | Total profit $286,397.02 | Overall profit margin 12.47% | Unique orders: 5,009 | Total quantity: 37,873
- **Nulls:** Zero null counts across all columns.
- **Duplicates:** Zero duplicate rows.

## Data quality audit and cleaning log
- **Initial inspection:** All 9994 rows loaded; zero nulls; zero duplicates.
- **Cleaning decisions:**
  - Worked on a copy (`clean = df.copy()`); source CSV never altered.
  - Derived `Profit Margin` = Profit / Sales (replacing divide-by-zero with NaN).
  - Derived `Order Month` and `Order Quarter` from `Order Date` for temporal grouping.
  - Derived `Is Loss` flag (Profit < 0).
- **No silent alterations:** The original `Dataset/Sample - Superstore.csv` remains untouched; all derived columns live in the copy.

## Methodology and definitions for key metrics
- **Profit margin** = Total Profit / Total Sales (across filtered data), expressed as percentage.
- **Loss-making orders** = row-level flag where Profit < 0.
- **Order count** = unique Order IDs (note: one order can have multiple line items; counts use unique Order IDs).
- **Monthly/quarterly trends** = grouped by `Order Month` / `Order Quarter` using pandas `dt.to_period`.

## Findings with actual numbers
1. **Sales $2,297,200.86 | Profit $286,397.02 | margin 12.47% | orders 5,009 | qty 37,873.**
2. **West** is the most profitable region ($108,418.45 profit); **Central** is the least ($39,706.36).
3. **Furniture** is the lowest-profit category ($18,451.27 profit on $742,000 sales); **Office Supplies** highest ($122,490.80).
4. **Tables** are the biggest loss-maker ($17,725.48 loss); **Texas** is the lossliest state ($25,729.36 loss).
5. **1,871 of 9,994 orders (18.7%)** lose money, totalling $156,131.29 in combined loss.
6. **Discount-profit correlation: -0.22** (negative association; not proof of causation).

## Charts
- `outputs/charts_retail.png` — 6-panel matrix: profit by region, sales/profit by category, lowest-profit sub-categories, monthly sales trend, discount vs profit scatter, orders by ship mode.

## Business recommendations
- Review >20% discount loss-making orders (esp. Tables/Bookcases); negotiate supplier costs.
- Investigate Texas, Ohio, Pennsylvania pricing/logistics for margin improvement.
- Target Furniture/Table category review to lift margin toward Office Supplies levels.

## Limitations and dataset mismatch
- Observational data: discount-profit link is association, not causation.
- Superstore is a synthetic/sample dataset; results may not generalize to a real retailer.
- Order ID does not uniquely identify a line item (one order spans multiple rows); counts below are unique Order ID counts.
- Single file; no customer-table enrichment or detailed demographic segmentation.

## Conclusion
The Superstore dataset is profitable overall (~12.5% margin) but driven by a few categories while a meaningful minority of order-lines lose money. Targeted discount review and category-specific pricing review are the clearest improvement levers.