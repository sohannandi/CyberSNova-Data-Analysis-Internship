# Project 5 — Human Resource Analytics

**Level:** Intermediate  
**Intern:** Sohan Nandi  
**Domain:** Data Analysis  
**Registration number:** CSN-OC-2026-474  
**Internship month/year:** October 2026  

## Dataset filename and source/attribution
- **File:** `Dataset/HR_comma_sep.csv`
- **Source:** Provided by the internship; a single-table human resources dataset containing satisfaction, evaluation, project count, monthly hours, tenure, work accidents, attrition (`left`), promotion, department, and salary band fields.

## Scope note (dataset mismatch vs task list)
The internship task list describes HR as a **four-file** dataset project (`Employee.csv`, `Salary.csv`, `Attendance.csv`, `Performance.csv`). The supplied download is a **single table** (`HR_comma_sep.csv`). The available fields include satisfaction, last evaluation, number of projects, monthly hours, time at company, work accidents, `left`, promotion history, department, and salary category — but do **not** necessarily include separate attendance or detailed performance records. Analysis uses only available fields; no records were invented, and missing tables were not fabricated.

## Business objective and questions
- What proportion of employees left?
- How does attrition vary by department and salary category?
- How are satisfaction, evaluation score, project count, monthly hours and tenure associated with attrition?
- How does attrition vary with promotion history or work-accident status?
- Which observed patterns may warrant further HR investigation?

## Dataset profile
- **Rows:** 14,999 raw records
- **Columns:** 10 (satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company, Work_accident, left, promotion_last_5years, Department, salary)
- **Descriptive statistics:** Attrition rate 23.81% (raw) / 16.60% (deduped). Satisfaction mean ~0.6; evaluation mean ~0.67.
- **Nulls:** Zero nulls.
- **Duplicates:** 3,008 exact duplicate rows detected and removed for primary analysis.

## Data quality audit and cleaning log
- **Duplicates:** 3,008 exact duplicate rows detected. Primary analysis performed on a **documented deduplicated copy** (11,991 rows). Raw and deduped attrition rates reported for transparency (23.81% vs 16.60%).
- **Key ranges validated:** satisfaction (0–1), evaluation (0–1), number_project (1–10), hours (80–400), tenure (1–20).
- **Dedup rationale:** Source has no guaranteed employee identifier; exact duplicates treated as potential redundant records. No unique ID-based deduplication performed.
- **No silent alterations:** Source CSV untouched; raw copy and deduped copy saved to `outputs/`.

## Methodology and definitions for key metrics
- **Attrition rate** = mean of `left` flag (1 = left, 0 = stayed).
- **Attrition by group** = mean `left` within group.
- **Dedup** = `drop_duplicates()` on the full row (exact matches).

## Findings with actual numbers
1. **Attrition rate:** 23.81% raw (3,571 / 14,999); 16.60% after dedup (1,991 / 11,991).
2. **Department:** HR 29.09%, Accounting 26.60%, Technical 25.63% (highest); Management 14.44%, RandD 15.37% (lowest).
3. **Salary:** low 29.69%, medium 20.43%, high 6.63% attrition (monotonically decreasing).
4. **Work accident:** 7.79% attrition (accident) vs 26.52% (no accident).
5. **Promotion:** 5.96% attrition (promoted) vs 24.20% (not promoted).

## Charts
- `outputs/charts_hr.png` — 6-panel matrix: attrition by department, attrition by salary, satisfaction by attrition, attrition by tenure, attrition by project count, attrition by monthly hours/work accident/promotion.

## Business recommendations
- Investigate HR, Accounting, Technical departments for culture/workload drivers.
- Review low/medium salary bands (compensation) to mitigate high attrition.
- Consider recognition and safety programs for accident-prevention retention.
- U-shaped project-count risk: very few (2) and very many (7) projects both show high attrition.
- Observational: associations, not causal claims.

## Limitations and dataset mismatch
- Single CSV; no separate attendance or detailed performance records as task list described (`Employee`, `Salary`, `Attendance`, `Performance`).
- Exact duplicates removed (3,008 rows); no employee ID to confirm they are true duplicates vs multiple records per person.
- Observational: associations shown, not causal claims (e.g., low satisfaction does not prove it caused leaving).
- Sensitive employee data: avoid publishing individual-level records in screenshots.
- Results on deduped data differ from raw (attrition rate 16.6% vs 23.8%); both reported for transparency.

## Conclusion
Attrition is highest in HR, Accounting, and Technical departments, and among low-salary employees. Work accident and promotion history show protective associations. Project count and monthly hours exhibit U-shaped risk. Further HR investigation recommended; deeper performance/attendance data would be needed.