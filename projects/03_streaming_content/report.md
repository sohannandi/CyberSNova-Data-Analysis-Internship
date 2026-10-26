# Project 3 — Movie Streaming Platform Analysis

**Level:** Beginner  
**Intern:** Sohan Nandi  
**Domain:** Data Analysis  
**Registration number:** CSN-OC-2026-474  
**Internship month/year:** October 2026  

## Dataset filename and source/attribution
- **File:** `Dataset/netflix_titles.csv`
- **Source:** Provided by the internship; a Netflix titles dataset (historical catalog snapshot) containing show metadata including type, release year, rating, duration, country, and genres.

## Business objective and questions
Analyze the Netflix catalog to answer:
- What is the split between movies and TV shows?
- How does content volume vary by release year and content type?
- Which genres/categories and countries appear most often where data is available?
- What are the patterns in ratings, movie durations and TV-show seasons?
- How has the catalog's release-year distribution changed?

## Dataset profile
- **Rows:** 8,807 titles
- **Columns:** 12 (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
- **Data types:** release_year integer; remaining descriptive fields strings; show_id string.
- **Descriptive statistics:** Movies 6,131 (69.6%) | TV Shows 2,676 (30.4%). Release years span 1925–2021 (90 distinct years).
- **Nulls:** director 2,634 | cast 825 | country 831 | date_added 10 | rating 4 | duration 3.
- **Duplicates:** Zero duplicate rows.

## Data quality audit and cleaning log
- **Initial inspection:** 8,807 rows; missing values concentrated in descriptive fields (director, cast, country).
- **Cleaning decisions:**
  - Missing director/cast filled with "Not listed" only as a display label (not imputed into analysis counts).
  - Missing rating filled with "Not rated" (display label only).
  - Whitespace in comma-separated country and genre fields normalized by stripping spaces.
  - `duration` parsed into numeric value + unit ("minutes" vs "seasons"); movie minutes and TV seasons kept SEPARATE and never compared directly.
  - No missing director, cast, country or rating values were replaced with invented values.
- **No silent alterations:** Source CSV untouched.

## Methodology and definitions for key metrics
- **Type split:** Count of `type == "Movie"` vs `"TV Show"`, reported with proportions.
- **Country/genre counts:** Exploded comma-separated fields; one title may count in multiple categories (counts can exceed total titles).
- **Duration parsing:** "X min" → minutes (movies); "N Seasons"/"N Season" → seasons (TV) — not directly comparable.
- **Missing values** treated as missing (not invented); reported explicitly.

## Findings with actual numbers
1. **Movies: 6,131 (69.6%) | TV Shows: 2,676 (30.4%).**
2. **Release years span 1925 to 2021 (90 distinct years).**
3. **Most common rating: TV-MA (3,207 titles); R-rated: 799.**
4. **Top country: United States (3,211 titles); top genre: International Movies (2,624 titles).**
5. **Median movie runtime ~99 minutes; median TV ~1 Season (NOT comparable units).**
6. **Director missing for 2,634 titles (29.9%); country missing for 831 — treated as missing, not invented.**

## Charts
- `outputs/charts_streaming.png` — 6-panel matrix: title type split, releases by year, top genres, rating distribution, top countries, movie duration histogram.

## Business recommendations
- Align acquisitions with top ratings/countries already present in the catalog.
- Keep movie minutes and TV seasons on **separate metrics**; never compare them directly.
- Investigate missing director/country fields if catalog completeness is a business requirement.

## Limitations and dataset mismatch
- Director/cast/country/rating missing values are treated as missing, never imputed with invented values.
- Comma-separated country/genre fields mean one title can count in multiple categories (counts can exceed total titles).
- Duration mixes "min" and "Seasons" formats — not directly comparable.
- Catalog snapshot (historical data), not a live feed; release-year distribution reflects catalog vintage, not viewership.
- "United States" vs " United States" whitespace variants exist; normalized during analysis.

## Conclusion
The catalog is movie-majority (~69.6%), with United States and India dominating country representation. Missing descriptive fields are handled explicitly rather than imputed, and movie minutes vs TV seasons are kept on separate scales to avoid misleading comparisons.