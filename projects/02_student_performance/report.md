# Project 2 — Student Academic Performance Analysis

**Level:** Beginner  
**Intern:** Sohan Nandi  
**Domain:** Data Analysis  
**Registration number:** CSN-OC-2026-474  
**Internship month/year:** October 2026  

## Dataset filename and source/attribution
- **File:** `Dataset/StudentsPerformance.csv`
- **Source:** Provided by the internship; a student performance survey dataset containing math, reading, and writing scores along with demographic and test-preparation attributes for 1,000 students.

## Business objective and questions
Compare student scores across subjects and demographic/preparation groups to answer:
- How do average math, reading and writing scores compare?
- How are scores associated with test-preparation completion?
- How do scores differ across gender, lunch type, parental education and race/ethnicity groups?
- Which groups show different score patterns across subjects?

## Dataset profile
- **Rows:** 1,000 students
- **Columns:** 8 (gender, race/ethnicity, parental level of education, lunch, test preparation course, math score, reading score, writing score)
- **Data types:** All score fields are integers 0–100; categorical fields are strings.
- **Descriptive statistics:** Math avg 66.09 | Reading avg 69.17 | Writing avg 68.05. Overall avg 66.54.
- **Nulls:** Zero null counts across all columns.
- **Duplicates:** Zero duplicate rows.

## Data quality audit and cleaning log
- **Initial inspection:** All 1,000 rows loaded; zero nulls; zero duplicates.
- **Cleaning decisions:**
  - Validated score ranges (0–100); all within bounds.
  - Derived `overall_score` as the simple mean of the three subject scores (transparent definition).
  - `overall_score` used only in descriptive analysis; subject scores used for primary group comparisons.
- **No silent alterations:** Source CSV untouched; derived column lives in analysis copy.

## Methodology and definitions for key metrics
- **Overall score** = (math score + reading score + writing score) / 3.
- Group comparisons report **average scores** alongside group sizes to avoid over-interpreting small subgroups.
- Correlation between subject scores reported cautiously as observational association.

## Findings with actual numbers
1. **Averages: math 66.09 | reading 69.17 | writing 68.05.**
2. **Test preparation completed vs none:** math +5.6 pts; reading +7.4 pts; writing +9.9 pts on average.
3. **Gender gap (math):** Males 68.73 vs Females 63.63; **Reading:** Females 72.61 vs Males 65.47; **Writing:** Females 72.47 vs Males 63.31.
4. **Lunch gap (math):** Standard lunch 70.03 vs free/reduced 58.92 (11.11-point difference).
5. **Math-reading correlation:** 0.82 (strong positive association).

## Charts
- `outputs/charts_student.png` — 6-panel matrix: score distributions by subject, avg scores by test preparation, avg scores by gender, overall score histogram, avg scores by lunch type, subject scatter matrix.

## Business recommendations
- Test preparation is associated with higher scores; explore expanding access (association, not causation).
- Consider subject-specific support: males for reading/writing, females for math (group averages only, observational).
- Students on free/reduced lunch score lower on average; investigate targeted tutoring/resources.

## Limitations and dataset mismatch
- Observational data: demographic attributes and test preparation are associated with scores, not causal.
- Group averages must not be used to predict individuals or reinforce stereotypes.
- Single cross-sectional snapshot; no longitudinal or causal inference.
- Data is observational; no intervention data available.

## Conclusion
Average scores sit in the mid-60s, reading and writing slightly above math. Test-preparation completion and lunch type show the largest group gaps. Any intervention must be framed as association, not causation.