# Project 4 — Telecom Customer Churn Analysis

**Level:** Intermediate  
**Intern:** Sohan Nandi  
**Domain:** Data Analysis  
**Registration number:** CSN-OC-2026-474  
**Internship month/year:** October 2026  

## Dataset filename and source/attribution
- **File:** `Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv`
- **Source:** Provided by the internship; a single customer-level Telco customer-churn dataset containing customer, service, contract, charge, and churn fields.

## Scope note (dataset mismatch vs task list)
The internship task list describes Telecom as a **three-file** dataset project (`Customers.csv`, `Customer_Usage.csv`, `Billing.csv`). The supplied download is **one CSV** per project — `WA_Fn-UseC_-Telco-Customer-Churn.csv`. All analysis below uses only columns actually present in this single file. No usage or billing tables were available. This limitation has been documented and requires coordinator confirmation before final submission.

## Business objective and questions
Analyze customer churn to answer:
- What is the churn rate?
- How does churn vary by contract, tenure, payment method, internet service and demographics?
- How do monthly charges and total charges differ between churned and retained customers?
- Which customer segments have higher observed churn rates?
- What retention opportunities are suggested by observed patterns?

## Dataset profile
- **Rows:** 7,043 customers
- **Columns:** 21 (customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn)
- **Descriptive statistics:** Churn rate 26.54% (1,869 churned / 7,043). Avg tenure 32.37 months. Avg monthly charge $64.76. Avg total charge $2,283.30.
- **Nulls:** Zero nulls as strings; `TotalCharges` contained 11 whitespace-only values.
- **Duplicates:** Zero duplicate rows.

## Data quality audit and cleaning log
- **customerID uniqueness:** All 7,043 customerIDs are unique (no duplicates). Validation passed.
- **TotalCharges blank handling:** `TotalCharges` is stored as string; 11 rows contain whitespace-only values (`488`, `753`, `936`, `1082`, `1340`, `3331`, `3826`, `4380`, `5218`, `6670`, `6754`). These were normalized to missing (`NaN`) via `pd.to_numeric(errors="coerce")`, then excluded from mean aggregations (documented below).
- **Churn target:** Inspected raw values ("Yes"/"No") before normalizing; no category substitution made.
- **No silent alterations:** Source CSV untouched; cleaned copy saved to `outputs/cleaned_telecom_churn.csv`.

## Methodology and definitions for key metrics
- **Churn rate** = count(Churn == "Yes") / total customers.
- **Churn by segment** = mean churn rate grouped by Contract / InternetService / PaymentMethod / tenure band.
- **Tenure bands:** 0–12, 12–24, 24–36, 36–48, 48–72, 72–100 months.
- **TotalCharges NaN handling:** 11 non-numeric rows excluded from aggregate means; treated as missing rather than dropped or imputed.

## Findings with actual numbers
1. **Churn rate:** 26.54% (1,869 of 7,043 customers).
2. **Contract:** Month-to-month churn 42.71% vs One year 11.27% vs Two year 2.83%.
3. **Internet service:** Fiber optic churn 41.89% vs DSL 18.96% vs No 7.40%.
4. **Payment method:** Electronic check churn 45.28% (highest); Credit card (automatic) 15.24% (lowest).
5. **Tenure:** 0–12 months churn 48.28% vs 72–100 months churn 1.66% (steep drop with tenure).
6. **Avg MonthlyCharges:** churned $70.35 vs retained $61.70; **Avg TotalCharges:** churned $941.81 vs retained $2,773.98.

## Charts
- `outputs/charts_telecom.png` — 6-panel matrix: churn rate by contract, churn rate by tenure band, churn rate by internet service, MonthlyCharges distribution by churn status, TotalCharges distribution by churn status, churn rate by InternetService × Contract segment.

## Business recommendations
- Prioritize retention offers for Month-to-month, Fiber optic, and Electronic check customers (highest churn segments).
- High churn in first year (0–12 months): design onboarding/loyalty program targeting early-tenure customers.
- Investigate Electronic check users — billing friction may drive churn; promote auto-pay transitions.
- Month-to-month is the dominant contract type (3,875 of 7,043); converting to longer contracts could materially reduce churn.

## Limitations and dataset mismatch
- Single customer-level CSV; no separate usage or billing tables as the task list described (`Customers.csv`, `Customer_Usage.csv`, `Billing.csv`).
- Observational: correlations shown, not causal drivers of churn.
- `TotalCharges` had 11 whitespace-only rows converted to NaN and excluded from means (documented above).
- No predictive model trained; segment rates are descriptive only.
- Coordinator confirmation requested: is the single-file version accepted for the Intermediate requirement?

## Conclusion
Churn is concentrated in month-to-month contracts, fiber-optic users, electronic-check payers, and early-tenure customers. Targeted retention in these segments is the clearest opportunity; deeper usage-level analysis requires the missing multi-file dataset (pending coordinator confirmation).