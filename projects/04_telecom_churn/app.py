"""Telecom Customer Churn Analysis - Interactive Streamlit Dashboard."""

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
    src = DATASET_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    assert src.exists(), f"Dataset file not found: {src}"
    df = pd.read_csv(src, encoding="utf-8")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["Churn"] = df["Churn"].astype(str).str.strip().map(lambda x: 1 if str(x).strip().lower() == "yes" else 0)
    return df


st.set_page_config(page_title="Telecom Churn Dashboard", layout="wide")

st.title("📞 Telecom Customer Churn Dashboard")
st.markdown(
    "**Level:** Intermediate  |  **Dataset:** `Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv`  "
    "|  **Intern:** Sohan Nandi (CSN-OC-2026-474)  |  **October 2026**"
)
st.caption(
    "Explore customer churn, contract behavior, service usage, and charges. "
    "Single customer-level file; descriptive analysis only — no predictive model applied."
)
st.markdown("---")

df = load_data()
clean = df.copy()
clean["tenure_band"] = pd.cut(
    clean["tenure"], bins=[0, 12, 24, 36, 48, 72, 100],
    labels=["0-12", "12-24", "24-36", "36-48", "48-72", "72-100"], right=False
)
clean.to_csv(OUT_DIR / "cleaned_telecom_churn.csv", index=False)

# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #
st.sidebar.header("Filters")
contract_sel = st.sidebar.multiselect(
    "Contract", options=sorted(clean["Contract"].dropna().unique()), default=sorted(clean["Contract"].dropna().unique())
)
internet_sel = st.sidebar.multiselect(
    "Internet Service", options=sorted(clean["InternetService"].dropna().unique()),
    default=sorted(clean["InternetService"].dropna().unique())
)
payment_sel = st.sidebar.multiselect(
    "Payment Method", options=sorted(clean["PaymentMethod"].dropna().unique()),
    default=sorted(clean["PaymentMethod"].dropna().unique())
)
tenure_band_sel = st.sidebar.multiselect(
    "Tenure Band", options=sorted(clean["tenure_band"].dropna().unique().astype(str)), default=sorted(clean["tenure_band"].dropna().unique().astype(str))
)
churn_filter = st.sidebar.selectbox("Churn status (view by)", options=["All", "Churned (Yes)", "Retained (No)"], index=0)

f = clean
if contract_sel:
    f = f[f["Contract"].isin(contract_sel)]
if internet_sel:
    f = f[f["InternetService"].isin(internet_sel)]
if payment_sel:
    f = f[f["PaymentMethod"].isin(payment_sel)]
if tenure_band_sel:
    f = f[f["tenure_band"].astype(str).isin(tenure_band_sel)]

if churn_filter != "All":
    f = f[f["Churn"] == (1 if churn_filter == "Churned (Yes)" else 0)]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# --------------------------------------------------------------------------- #
# KPIs
# --------------------------------------------------------------------------- #
st.subheader("Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{len(f):,}")
c2.metric("Churn Rate", f"{(f['Churn']==1).mean()*100:.1f}%")
c3.metric("Avg Tenure", f"{f['tenure'].mean():.1f} months")
c4.metric("Avg Monthly Charge", f"${f['MonthlyCharges'].mean():.2f}")

# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
st.subheader("Churn Rate by Contract, Internet Service, Tenure")
c1, c2 = st.columns(2)
with c1:
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    cr = f.groupby("Contract")["Churn"].apply(lambda s: (s==1).mean())
    if not cr.empty:
        cr.sort_values().plot(kind="barh", ax=ax1, color="#d62728")
        ax1.set_title("Churn Rate by Contract"); ax1.set_xlabel("Churn Rate")
        st.pyplot(fig1, use_container_width=True)
with c2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    cr2 = f.groupby("InternetService")["Churn"].apply(lambda s: (s==1).mean())
    if not cr2.empty:
        cr2.sort_values().plot(kind="barh", ax=ax2, color="#1f77b4")
        ax2.set_title("Churn Rate by Internet Service"); ax2.set_xlabel("Churn Rate")
        st.pyplot(fig2, use_container_width=True)

st.subheader("Churn Rate by Tenure Band")
fig3, ax3 = plt.subplots(figsize=(8, 4))
cr3 = f.groupby("tenure_band")["Churn"].apply(lambda s: (s==1).mean())
if not cr3.empty:
    cr3.plot(kind="bar", ax=ax3, color="#ff7f0e")
    ax3.set_title("Churn Rate by Tenure Band"); ax3.set_xlabel("Tenure Band"); ax3.set_ylabel("Churn Rate")
    ax3.tick_params(axis="x", rotation=0)
    st.pyplot(fig3, use_container_width=True)

st.subheader("Charges by Churn Status")
c1, c2 = st.columns(2)
with c1:
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    sub = f.groupby("Churn")[["MonthlyCharges", "TotalCharges"]].mean()
    status_labels = {0: "Retained", 1: "Churned"}
    status_colors = {0: "#2ca02c", 1: "#d62728"}
    plotted_statuses = []
    for status in (0, 1):
        if status in sub.index:
            sub.loc[status].plot(kind="bar", ax=ax4, color=status_colors[status])
            plotted_statuses.append(status_labels[status])
    if plotted_statuses:
        ax4.set_title("Avg Charges by Churn Status")
        ax4.set_ylabel("Avg ($)")
        ax4.legend(plotted_statuses)
    st.pyplot(fig4, use_container_width=True)
with c2:
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    sub2 = f.groupby("PaymentMethod")["Churn"].apply(lambda s: (s==1).mean()).sort_values()
    if not sub2.empty:
        sub2.plot(kind="barh", ax=ax5, color="#9467bd")
        ax5.set_title("Churn Rate by Payment Method"); ax5.set_xlabel("Churn Rate")
        st.pyplot(fig5, use_container_width=True)

# --------------------------------------------------------------------------- #
# Key findings
# --------------------------------------------------------------------------- #
st.markdown("---")
st.subheader("Key Findings")
st.markdown(f"- **Overall churn rate:** {(f['Churn']==1).mean()*100:.1f}% ({int((f['Churn']==1).sum())} of {len(f)}).")
cr_month = f.loc[f["Contract"]=="Month-to-month", "Churn"].mean() if "Month-to-month" in f["Contract"].values else 0
cr_two = f.loc[f["Contract"]=="Two year", "Churn"].mean() if "Two year" in f["Contract"].values else 0
st.markdown(f"- **Month-to-month churn:** {cr_month:.1%} vs **Two year:** {cr_two:.1%}.")
cr_fib = f.loc[f["InternetService"]=="Fiber optic", "Churn"].mean() if "Fiber optic" in f["InternetService"].values else 0
st.markdown(f"- **Fiber optic churn:** {cr_fib:.1%}.")
cr_e = f.loc[f["PaymentMethod"]=="Electronic check", "Churn"].mean() if "Electronic check" in f["PaymentMethod"].values else 0
st.markdown(f"- **Electronic check churn:** {cr_e:.1%} (highest among observed payment methods).")
st.markdown(f"- **Avg MonthlyCharge (churned):** ${f.loc[f['Churn']==1,'MonthlyCharges'].mean():.2f} vs Retained: ${f.loc[f['Churn']==0,'MonthlyCharges'].mean():.2f}.")

with st.expander("Data preview (first 10 rows)"):
    st.dataframe(f.head(10).reset_index(drop=True), use_container_width=True)

st.caption(
    "Data source: Telco customer churn dataset (`Dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv`). "
    "Single customer-level table; task list described Customers/Usage/Billing split — not available. "
    "Descriptive analysis only; no predictive model applied."
)