# CyberSNova-Data-Analysis-Internship

CyberSNova Data Analysis Internship featuring 5 projects in Retail Sales, Student Performance, Netflix Content, Telecom Churn, and HR Analytics using Python, Pandas, and Streamlit.

**Organization:** CyberSNova  
**Domain:** Data Analysis  
**Intern:** Sohan Nandi  
**Registration number:** CSN-OC-2026-474  
**Internship period:** October 2026  

This repository contains five reproducible data-analysis projects built with a Python-first
analytics stack (pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Jupyter, pytest).

---

## 1. Project overview and the five selected projects

The final project implements five projects from the internship brief, each containing data
validation/cleaning, exploratory analysis, meaningful visualizations, an interactive dashboard,
a written report, and screenshot evidence.

### Beginner level — complete all three
1. **Retail Sales Performance Analysis** — `Dataset/Sample - Superstore.csv`  
   Business questions around regions, categories, sub-categories, time trends, discounts, shipping.
2. **Student Academic Performance Analysis** — `Dataset/StudentsPerformance.csv`  
   Compare math/reading/writing scores, test-preparation association, demographic patterns.
3. **Movie Streaming Platform Analysis** — `Dataset/netflix_titles.csv`  
   Movie vs TV split, release-year trends, genres, countries, ratings, duration patterns.

### Intermediate level — implement both, subject to dataset-scope confirmation
4. **Telecom Customer Churn Analysis** — `Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv`  
   Single-file churn analysis (task list described Customers/Usage/Billing split).
5. **Human Resource Analytics** — `Dataset/HR_comma_sep.csv`  
   Single-table attrition analysis (task list described Employee/Salary/Attendance/Performance split).

---

## 2. Dataset file mapping and scope caveats

| Project | Relative path | Task list file(s) | Status |
|---|---|---|---|
| Retail Sales | `Dataset/Sample - Superstore.csv` | — | Single file (retail), directly suitable |
| Student Performance | `Dataset/StudentsPerformance.csv` | — | Single file (student survey), directly suitable |
| Streaming Content | `Dataset/netflix_titles.csv` | — | Single file (catalog), directly suitable |
| Telecom Churn | `Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv` | 3-file split (`Customers`, `Usage`, `Billing`) | **Mismatch** — supplied is a single customer-level table; multi-file scope not available. Clearly disclosed; coordinator confirmation requested. |
| HR Analytics | `Dataset/HR_comma_sep.csv` | 4-file split (`Employee`, `Salary`, `Attendance`, `Performance`) | **Mismatch** — supplied is a single table; attendance/performance splits not available. Clearly disclosed; coordinator confirmation requested. |

**Important internship-rule note:** The task list describes Telecom as a three-file dataset
project and HR as a four-file dataset project. The currently supplied downloads are one CSV per
project. The analyses therefore build on the **actual columns in those files** and do **not** invent
missing tables, fields, or records. The dataset-scope differences for Telecom and HR are documented
in each project's `report.md`, and the internship coordinator should confirm whether the supplied
single-file versions are accepted for the Intermediate requirements before final submission.

---

## 3. Python environment setup

Requires **Python 3.11** or compatible version.

```bash
python --version   # should be 3.11+
```

### Create and activate a virtual environment (from the `CyberNova/` directory)

```bash
python -m venv .venv
```

**Windows PowerShell activation:**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux activation:**

```bash
source .venv/bin/activate
```

## 4. Dependency installation

```bash
pip install -r requirements.txt
```

Installed packages (as of the final submission): pandas, NumPy, Matplotlib, Seaborn, Plotly,
Streamlit, Jupyter, nbconvert, pytest, ipykernel.

## 5. How to run each Streamlit dashboard

Run one dashboard at a time from the `CyberNova/` directory (with the venv active):

```bash
streamlit run projects/01_retail_sales/app.py
streamlit run projects/02_student_performance/app.py
streamlit run projects/03_streaming_content/app.py
streamlit run projects/04_telecom_churn/app.py
streamlit run projects/05_hr_analytics/app.py
```

Each dashboard includes: KPI cards, filters, charts, a data preview, and a computed key-findings
section. Filters update KPIs and charts consistently; empty filter results are handled gracefully.

## 6. How to open and run notebooks

Each project has `analysis.ipynb` under `projects/<id>_<name>/`. The notebook is valid and executed
(see the executed notebook cells' outputs).

From the `CyberNova/` directory, with the venv active:

- **Jupyter Lab:** `jupyter lab`
- **Jupyter Notebook:** `jupyter notebook`
- **Execute via nbconvert:** `python -m nbconvert --to notebook --execute --output analysis.ipynb projects/<project>/analysis.ipynb`

or open the notebook directly in Jupyter and run it.

Each notebook follows a consistent sequence:
1. Objective and business questions (markdown).
2. Imports and reproducibility setup (code).
3. Load source data (code).
4. Inspect dimensions, columns, types and sample records (code).
5. Data-quality audit (code).
6. Cleaning and validation (code).
7. Exploratory data analysis (code).
8. Charts and interpretations (code).
9. Findings and recommendations (code).
10. Limitations and conclusion (code).

## 7. Output / report / screenshot locations

```text
CyberNova/
├── Dataset/
├── projects/
│   ├── <id>_<name>/
│       ├── analysis.ipynb
│       ├── app.py
│       ├── report.md
│       └── outputs/
├── src/
├── tests/
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

Each project's `outputs/` folder contains cleaned/derived data (CSV) and chart images (PNG) as
generated by the executed notebooks:
- `outputs/cleaned_*.csv` — cleaned/derived datasets.
- `outputs/charts_*.png` — Matplotlib/Seaborn chart images.

## 8. Data cleaning decisions and test commands

Cleaning decisions are documented per project in each `report.md` and visible in each notebook.

Run the basic data-validation tests:

```bash
pytest -q
```

Expected result: **20 passed**.

Tests verify:
- Each expected source file exists.
- Each CSV can be loaded.
- Required project columns exist; missing columns produce informative errors.
- Data-cleaning functions do not mutate the original DataFrame unexpectedly.
- Numeric conversion and missing-value handling work for relevant columns.
- HR deduplication is documented and reproducible.
- Dashboard entry points have no syntax errors.

## 9. How to interpret metrics and limitations

All metrics are computed live from the source data; no values are hardcoded into dashboard
components. Metrics should be interpreted as:
- **Descriptive**: group rates (churn, attrition, margins) are observed rates, not causal claims.
- **Associational**: correlations (e.g., discount–profit, satisfaction–attrition) are descriptive.
- **Observational**: datasets are observational; no causation is claimed without causal design.
- **Comparative**: group averages may not generalize to individuals or larger populations.

## 10. Commands reference (from `CyberNova/`)

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell activation
pip install -r requirements.txt
streamlit run projects/01_retail_sales/app.py
streamlit run projects/02_student_performance/app.py
streamlit run projects/03_streaming_content/app.py
streamlit run projects/04_telecom_churn/app.py
streamlit run projects/05_hr_analytics/app.py
python -m nbconvert --to notebook --execute --output analysis.ipynb projects/<project>/analysis.ipynb
pytest -q
```
