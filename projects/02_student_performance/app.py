"""Student Academic Performance Analysis - Interactive Streamlit Dashboard."""

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
    src = DATASET_DIR / "StudentsPerformance.csv"
    assert src.exists(), f"Dataset file not found: {src}"
    df = pd.read_csv(src, encoding="utf-8")
    return df


st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📚 Student Academic Performance Dashboard")
st.markdown(
    "**Level:** Beginner  |  **Dataset:** `Dataset/StudentsPerformance.csv`  "
    "|  **Intern:** Sohan Nandi (CSN-OC-2026-474)  |  **October 2026**"
)
st.caption(
    "Compare math, reading, and writing scores across demographics and test-preparation status. "
    "All values are computed from the loaded dataset. Observational — not causal."
)
st.markdown("---")

df = load_data()
clean = df.copy()
clean["overall_score"] = clean[["math score", "reading score", "writing score"]].mean(axis=1)
clean.to_csv(OUT_DIR / "cleaned_student_performance.csv", index=False)

# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #
st.sidebar.header("Filters")
gender_sel = st.sidebar.multiselect(
    "Gender", options=sorted(clean["gender"].unique()), default=sorted(clean["gender"].unique())
)
race_sel = st.sidebar.multiselect(
    "Race/Ethnicity", options=sorted(clean["race/ethnicity"].unique()), default=sorted(clean["race/ethnicity"].unique())
)
edu_sel = st.sidebar.multiselect(
    "Parental Education", options=sorted(clean["parental level of education"].unique()),
    default=sorted(clean["parental level of education"].unique())
)
lunch_sel = st.sidebar.multiselect(
    "Lunch Type", options=sorted(clean["lunch"].unique()), default=sorted(clean["lunch"].unique())
)
prep_sel = st.sidebar.multiselect(
    "Test Preparation", options=sorted(clean["test preparation course"].unique()),
    default=sorted(clean["test preparation course"].unique())
)

f = clean
if gender_sel:
    f = f[f["gender"].isin(gender_sel)]
if race_sel:
    f = f[f["race/ethnicity"].isin(race_sel)]
if edu_sel:
    f = f[f["parental level of education"].isin(edu_sel)]
if lunch_sel:
    f = f[f["lunch"].isin(lunch_sel)]
if prep_sel:
    f = f[f["test preparation course"].isin(prep_sel)]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# --------------------------------------------------------------------------- #
# KPIs
# --------------------------------------------------------------------------- #
st.subheader("Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Students", f"{len(f):,}")
c2.metric("Avg Math", f"{f['math score'].mean():.1f}")
c3.metric("Avg Reading", f"{f['reading score'].mean():.1f}")
c4.metric("Avg Writing", f"{f['writing score'].mean():.1f}")

# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
st.subheader("Score Distributions")
fig1, ax1 = plt.subplots(figsize=(10, 4))
for subj, col in zip(["math score", "reading score", "writing score"], ["#1f77b4", "#ff7f0e", "#2ca02c"]):
    f[subj].plot(kind="hist", bins=15, ax=ax1, alpha=0.5, label=subj.replace(" score", ""), color=col, edgecolor="white")
ax1.set_xlabel("Score")
ax1.set_ylabel("Count")
ax1.set_title("Score Distributions by Subject")
ax1.legend()
st.pyplot(fig1, use_container_width=True)

st.subheader("Average Scores by Test Preparation")
fig2, ax2 = plt.subplots(figsize=(8, 4))
g = f.groupby("test preparation course")[["math score", "reading score", "writing score"]].mean()
if not g.empty:
    g.plot(kind="bar", ax=ax2, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
    ax2.set_title("Subject Averages by Test Preparation")
    ax2.set_ylabel("Average Score")
    ax2.tick_params(axis="x", rotation=0)
    ax2.legend()
st.pyplot(fig2, use_container_width=True)

st.subheader("Scores by Gender & Lunch Type")
c1, c2 = st.columns(2)
with c1:
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    g = f.groupby("gender")[["math score", "reading score", "writing score"]].mean()
    if not g.empty:
        g.plot(kind="bar", ax=ax3, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
        ax3.set_title("Average Scores by Gender")
        ax3.set_ylabel("Average Score")
        ax3.tick_params(axis="x", rotation=0)
        ax3.legend()
    st.pyplot(fig3, use_container_width=True)
with c2:
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    g = f.groupby("lunch")[["math score", "reading score", "writing score"]].mean()
    if not g.empty:
        g.plot(kind="bar", ax=ax4, color=["#d62728", "#9467bd"])
        ax4.set_title("Average Scores by Lunch Type")
        ax4.set_ylabel("Average Score")
        ax4.tick_params(axis="x", rotation=0)
        ax4.legend()
    st.pyplot(fig4, use_container_width=True)

st.subheader("Overall Score Distribution & Subject Correlations")
c1, c2 = st.columns(2)
with c1:
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    f["overall_score"].plot(kind="hist", bins=15, ax=ax5, color="#2ca02c", edgecolor="white", alpha=0.7)
    ax5.set_title("Overall Score Distribution")
    ax5.set_xlabel("Overall Score")
    st.pyplot(fig5, use_container_width=True)
with c2:
    fig6, ax6 = plt.subplots(figsize=(7, 4))
    subs = ["math score", "reading score", "writing score"]
    pd.plotting.scatter_matrix(f[subs], ax=ax6, figsize=(6, 6), diagonal="kde", color="#9467bd", alpha=0.4)
    ax6.set_title("Subject Score Scatter Matrix")
    st.pyplot(fig6, use_container_width=True)

# --------------------------------------------------------------------------- #
# Key findings
# --------------------------------------------------------------------------- #
st.markdown("---")
st.subheader("Key Findings")
g_prep = f.groupby("test preparation course")[["math score", "reading score", "writing score"]].mean()
diff_math = g_prep.loc["completed", "math score"] - g_prep.loc["none", "math score"] if "completed" in g_prep.index and "none" in g_prep.index else 0
diff_read = g_prep.loc["completed", "reading score"] - g_prep.loc["none", "reading score"] if "completed" in g_prep.index and "none" in g_prep.index else 0
diff_writ = g_prep.loc["completed", "writing score"] - g_prep.loc["none", "writing score"] if "completed" in g_prep.index and "none" in g_prep.index else 0
corr_mr = f["math score"].corr(f["reading score"])
st.markdown(f"- **Test preparation** is associated with **+{diff_math:.1f} math**, **+{diff_read:.1f} reading**, **+{diff_writ:.1f} writing** points on average.")
st.markdown(f"- **Math-reading correlation:** {corr_mr:.2f} (strong positive association).")
male_m = f.loc[f.gender=="male", "math score"].mean() if "male" in f.gender.unique() else 0
female_m = f.loc[f.gender=="female", "math score"].mean() if "female" in f.gender.unique() else 0
st.markdown(f"- **Gender gap (math):** Males {male_m:.1f} vs Females {female_m:.1f}.")
lunch_math = f.loc[f.lunch=="standard", "math score"].mean() - f.loc[f.lunch=="free/reduced", "math score"].mean() if "standard" in f.lunch.unique() and "free/reduced" in f.lunch.unique() else 0
st.markdown(f"- **Lunch type gap (math):** Standard lunch students score **{lunch_math:.1f} points higher** on average.")

with st.expander("Data preview (first 10 rows)"):
    st.dataframe(f.head(10).reset_index(drop=True), use_container_width=True)

st.caption(
    "Data source: UCI Student Performance dataset (`Dataset/StudentsPerformance.csv`). "
    "Observational — group associations do not imply causation."
)