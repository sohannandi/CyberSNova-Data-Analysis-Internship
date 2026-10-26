"""Human Resource Analytics - Interactive Streamlit Dashboard."""

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")


def resolve_repo_root():
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "Dataset").is_dir() and (parent / "projects").is_dir():
            return parent
        if (parent / "Dataset").is_dir():
            return parent
    return Path(__file__).resolve().parents[3]


REPO_ROOT = resolve_repo_root()
DATASET_DIR = REPO_ROOT / "Dataset"
OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


@st.cache_data
def load_data():
    src = DATASET_DIR / "HR_comma_sep.csv"
    assert src.exists(), f"Dataset file not found: {src}"
    df = pd.read_csv(src, encoding="latin1")
    return df


st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("Human Resource Analytics Dashboard")
st.markdown(
    "**Level:** Intermediate  |  **Dataset:** `Dataset/HR_comma_sep.csv`  "
    "|  **Intern:** Sohan Nandi (CSN-OC-2026-474)  |  **October 2026**"
)
st.caption(
    "Explore employee attrition across departments, salary, satisfaction, tenure, and work patterns. "
    "Descriptive analysis only - associations are not causal."
)
st.markdown("---")

raw = load_data()

raw_dup_count = int(raw.duplicated().sum())
clean = raw.drop_duplicates().copy()
st.sidebar.markdown(f"**Data-quality note:** {raw_dup_count} exact duplicate rows removed (raw {len(raw)} -> dedup {len(clean)}).")

clean.to_csv(OUT_DIR / "cleaned_hr_analytics.csv", index=False)
raw.to_csv(OUT_DIR / "cleaned_hr_analytics_raw.csv", index=False)

st.sidebar.header("Filters")
dept_sel = st.sidebar.multiselect(
    "Department", options=sorted(clean["Department"].unique()), default=sorted(clean["Department"].unique())
)
salary_sel = st.sidebar.multiselect(
    "Salary Category (band)", options=["low", "medium", "high"], default=["low", "medium", "high"]
)
tenure_range = st.sidebar.slider(
    "Time at company (years)",
    min_value=int(clean["time_spend_company"].min()),
    max_value=int(clean["time_spend_company"].max()),
    value=(int(clean["time_spend_company"].min()), int(clean["time_spend_company"].max())),
)
satisfaction_range = st.sidebar.slider(
    "Satisfaction level", 0.0, 1.0, (0.0, 1.0), step=0.05
)

f = clean
if dept_sel:
    f = f[f["Department"].isin(dept_sel)]
if salary_sel:
    f = f[f["salary"].isin(salary_sel)]
f = f[(f["time_spend_company"] >= tenure_range[0]) & (f["time_spend_company"] <= tenure_range[1])]
f = f[(f["satisfaction_level"] >= satisfaction_range[0]) & (f["satisfaction_level"] <= satisfaction_range[1])]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

st.subheader("Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Employee Records", f"{len(f):,}")
c2.metric("Attrition Rate", f"{f['left'].mean()*100:.1f}%")
c3.metric("Avg Satisfaction", f"{f['satisfaction_level'].mean():.2f}")
c4.metric("Avg Evaluation", f"{f['last_evaluation'].mean():.2f}")

st.subheader("Attrition by Department & Salary")
c1, c2 = st.columns(2)
with c1:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sub = f.groupby("Department")["left"].mean().sort_values(ascending=True)
    if not sub.empty:
        sub.plot(kind="barh", ax=ax1, color="#d62728")
        ax1.set_title("Attrition Rate by Department"); ax1.set_xlabel("Attrition Rate")
    st.pyplot(fig1, use_container_width=True)
with c2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sub2 = f.groupby("salary")["left"].mean().sort_values(ascending=True)
    if not sub2.empty:
        sub2.plot(kind="barh", ax=ax2, color="#ff7f0e")
        ax2.set_title("Attrition Rate by Salary Category"); ax2.set_xlabel("Attrition Rate")
    st.pyplot(fig2, use_container_width=True)

st.subheader("Satisfaction, Tenure & Projects vs Attrition")
c1, c2 = st.columns(2)
with c1:
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    for val, col, label in [(1, "#d62728", "Left"), (0, "#2ca02c", "Stayed")]:
        f.loc[f["left"]==val, "satisfaction_level"].plot(kind="hist", bins=20, ax=ax3, alpha=0.5, color=col, label=label, edgecolor="white")
    ax3.set_title("Satisfaction Level by Attrition"); ax3.set_xlabel("Satisfaction"); ax3.legend()
    st.pyplot(fig3, use_container_width=True)
with c2:
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sub3 = f.groupby("time_spend_company")["left"].mean()
    if not sub3.empty:
        sub3.plot(kind="bar", ax=ax4, color="#1f77b4")
        ax4.set_title("Attrition Rate by Tenure"); ax4.set_xlabel("Years at Company"); ax4.set_ylabel("Attrition Rate")
        ax4.tick_params(axis="x", rotation=0)
    st.pyplot(fig4, use_container_width=True)

st.subheader("Project Count & Work-accident Status")
c1, c2 = st.columns(2)
with c1:
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    sub4 = f.groupby("number_project")["left"].mean()
    if not sub4.empty:
        sub4.plot(kind="bar", ax=ax5, color="#9467bd")
        ax5.set_title("Attrition Rate by Number of Projects"); ax5.set_xlabel("Projects"); ax5.set_ylabel("Attrition Rate")
        ax5.tick_params(axis="x", rotation=0)
    st.pyplot(fig5, use_container_width=True)
with c2:
    fig6, ax6 = plt.subplots(figsize=(8, 4))
    acc_sub = f.groupby("average_montly_hours")["left"].mean()
    if not acc_sub.empty:
        acc_sub.plot(kind="line", ax=ax6, color="#8c564b")
        ax6.set_title("Attrition Rate by Avg Monthly Hours"); ax6.set_xlabel("Avg Monthly Hours"); ax6.set_ylabel("Attrition Rate")
    st.pyplot(fig6, use_container_width=True)

st.markdown("---")
st.subheader("Key Findings")
st.markdown(f"- **Attrition rate:** {f['left'].mean()*100:.1f}% ({int(f['left'].sum())} of {len(f)} employees).")
top_dept = f.groupby("Department")["left"].mean().idxmax()
st.markdown(f"- **Highest-attrition department:** {top_dept} ({f.groupby('Department')['left'].mean().max()*100:.1f}%).")
salary_rates = f.groupby("salary")["left"].mean()
salary_summary = " | ".join(
    f"{band} {salary_rates[band] * 100:.1f}%"
    for band in ("low", "medium", "high")
    if band in salary_rates.index
)
st.markdown(f"- **Attrition by salary:** {salary_summary}.")
st.markdown(f"- **Satisfaction:** employees who left average {f.loc[f['left']==1,'satisfaction_level'].mean():.2f}; those who stayed average {f.loc[f['left']==0,'satisfaction_level'].mean():.2f}.")
st.markdown(f"- **Work accident:** employees with an accident show {f.groupby('Work_accident')['left'].mean().get(1,0)*100:.1f}% attrition vs {f.groupby('Work_accident')['left'].mean().get(0,0)*100:.1f}% without.")
st.markdown(f"- **Promotion:** {f.groupby('promotion_last_5years')['left'].mean().get(1,0)*100:.1f}% attrition among promoted vs {f.groupby('promotion_last_5years')['left'].mean().get(0,0)*100:.1f}% among not promoted.")
st.markdown("- **Observational:** associations, not causal claims (e.g., low satisfaction does not prove it caused leaving).")

with st.expander("Data preview (first 10 rows)"):
    st.dataframe(f.head(10).reset_index(drop=True), use_container_width=True)

st.caption(
    "Data source: HR dataset (`Dataset/HR_comma_sep.csv`). "
    "3008 exact duplicate rows removed for primary analysis; no employee identifier exists. "
    "Task list described Employee/Salary/Attendance/Performance splits - not available in this file."
)
