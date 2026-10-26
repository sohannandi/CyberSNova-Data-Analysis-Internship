"""Retail Sales Performance Analysis - Interactive Streamlit Dashboard.

Dashboard entry point for the Superstore retail sales dataset.
Run from the CyberNova/ repo root:
    streamlit run projects/01_retail_sales/app.py
"""

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")


# --------------------------------------------------------------------------- #
# Path resolution (works from repo root or from this project folder)
# --------------------------------------------------------------------------- #
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
    """Load the Superstore source CSV with correct encoding + date parsing."""
    src = DATASET_DIR / "Sample - Superstore.csv"
    assert src.exists(), f"Dataset file not found: {src}"
    df = pd.read_csv(src, encoding="latin1", parse_dates=["Order Date", "Ship Date"])
    return df


# --------------------------------------------------------------------------- #
# App layout
# --------------------------------------------------------------------------- #
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

st.title("🛒 Retail Sales Performance Dashboard")
st.markdown(
    "**Level:** Beginner  |  **Dataset:** `Dataset/Sample - Superstore.csv`  "
    "|  **Intern:** Sohan Nandi (CSN-OC-2026-474)  |  **October 2026**"
)
st.caption(
    "Interactive exploration of sales and profit across regions, categories, and time. "
    "All values are computed live from the loaded dataset."
)
st.markdown("---")

# Load + clean
df = load_data()
clean = df.copy()
import numpy as np
clean["Profit Margin"] = clean["Profit"] / clean["Sales"].replace(0, np.nan)
clean["Order Month"] = clean["Order Date"].dt.to_period("M").dt.to_timestamp()
clean["Order Quarter"] = clean["Order Date"].dt.to_period("Q").dt.to_timestamp()
clean["Is Loss"] = clean["Profit"] < 0

# Save cleaned data once
clean.to_csv(OUT_DIR / "cleaned_retail_sales.csv", index=False)

# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Order date range",
    value=(clean["Order Date"].min().date(), clean["Order Date"].max().date()),
    help="Restrict to orders within a date window.",
)
# normalize to a tuple of timestamps
if isinstance(date_range, tuple) and len(date_range) == 2:
    d_start, d_end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    d_start, d_end = clean["Order Date"].min(), clean["Order Date"].max()

region_sel = st.sidebar.multiselect(
    "Region", options=sorted(clean["Region"].unique()), default=sorted(clean["Region"].unique())
)
cat_sel = st.sidebar.multiselect(
    "Category", options=sorted(clean["Category"].unique()), default=sorted(clean["Category"].unique())
)
segment_sel = st.sidebar.multiselect(
    "Customer Segment", options=sorted(clean["Segment"].unique()), default=sorted(clean["Segment"].unique())
)
ship_sel = st.sidebar.multiselect(
    "Ship Mode", options=sorted(clean["Ship Mode"].unique()), default=sorted(clean["Ship Mode"].unique())
)

f = clean
if region_sel:
    f = f[f["Region"].isin(region_sel)]
if cat_sel:
    f = f[f["Category"].isin(cat_sel)]
if segment_sel:
    f = f[f["Segment"].isin(segment_sel)]
if ship_sel:
    f = f[f["Ship Mode"].isin(ship_sel)]
f = f[(f["Order Date"] >= d_start) & (f["Order Date"] <= d_end)]

if f.empty:
    st.warning("No records match the selected filters. Please adjust the filters.")
    st.stop()

# --------------------------------------------------------------------------- #
# KPI cards
# --------------------------------------------------------------------------- #
total_sales = f["Sales"].sum()
total_profit = f["Profit"].sum()
margin = (total_profit / total_sales * 100) if total_sales else 0
orders = f["Order ID"].nunique()
quantity = f["Quantity"].sum()
loss_orders = int(f["Is Loss"].sum())

st.subheader("Key Metrics")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Orders", f"{orders:,}")
c5.metric("Quantity", f"{quantity:,}")
c6.metric("Loss-making", f"{loss_orders} ({loss_orders/len(f)*100:.1f}%)")

# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
st.subheader("Sales & Profit Trends")
monthly = f.groupby("Order Month")[["Sales", "Profit"]].sum()
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)
if not monthly.empty:
    ax.plot(monthly.index, monthly["Sales"], marker="o", label="Sales", color="#1f77b4")
    ax2 = ax.twinx()
    ax2.plot(monthly.index, monthly["Profit"], marker="s", label="Profit", color="#d62728")
    ax.set_ylabel("Sales ($)", color="#1f77b4")
    ax2.set_ylabel("Profit ($)", color="#d62728")
    ax.set_title("Monthly Sales and Profit")
    ax.tick_params(axis="x", rotation=45)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
st.pyplot(fig, use_container_width=True)

st.subheader("Performance by Category & Region")
c1, c2 = st.columns(2)
with c1:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    sub = f.groupby("Category")[["Sales", "Profit"]].sum()
    if not sub.empty:
        sub.plot(kind="bar", ax=ax2, color=["#2ca02c", "#d62728"])
        ax2.set_title("Sales & Profit by Category")
        ax2.set_ylabel("Amount ($)")
        ax2.tick_params(axis="x", rotation=20)
        ax2.legend()
    st.pyplot(fig2, use_container_width=True)
with c2:
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    sub = f.groupby("Region")["Profit"].sum().sort_values()
    if not sub.empty:
        sub.plot(kind="barh", ax=ax3, color="#1f77b4")
        ax3.set_title("Profit by Region")
        ax3.set_xlabel("Profit ($)")
    st.pyplot(fig3, use_container_width=True)

st.subheader("Sub-Category Profit (bottom 10) & Discount vs Profit")
c1, c2 = st.columns(2)
with c1:
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    bot = f.groupby("Sub-Category")["Profit"].sum().sort_values().head(8)
    if not bot.empty:
        bot.plot(kind="barh", ax=ax4, color="#d62728")
        ax4.set_title("Lowest-Profit Sub-Categories")
        ax4.set_xlabel("Profit ($)")
    st.pyplot(fig4, use_container_width=True)
with c2:
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    samp = f.sample(n=min(1500, len(f)), random_state=1)
    ax5.scatter(samp["Discount"], samp["Profit"], alpha=0.5, s=10, color="#ff7f0e")
    ax5.set_title("Discount vs Profit (sample)")
    ax5.set_xlabel("Discount")
    ax5.set_ylabel("Profit ($)")
    st.pyplot(fig5, use_container_width=True)

st.subheader("Orders by Ship Mode")
fig6, ax6 = plt.subplots(figsize=(8, 4))
f["Ship Mode"].value_counts().plot(kind="bar", ax=ax6, color="#7f7f7f")
ax6.set_title("Orders by Ship Mode")
ax6.set_ylabel("Count")
ax6.tick_params(axis="x", rotation=20)
st.pyplot(fig6, use_container_width=True)

# --------------------------------------------------------------------------- #
# Key findings (computed from filtered data)
# --------------------------------------------------------------------------- #
st.markdown("---")
st.subheader("Key Findings")
top_region = f.groupby("Region")["Profit"].sum().idxmax()
bot_subcat = f.groupby("Sub-Category")["Profit"].sum().idxmin()
disc_corr = f["Discount"].corr(f["Profit"]) if len(f) > 1 else float("nan")
st.markdown(
    f"- **{top_region}** is the most profitable region "
    f"(${f.groupby('Region')['Profit'].sum().max():,.0f} profit)."
)
st.markdown(
    f"- **{bot_subcat}** is the lowest-profit sub-category "
    f"(${f.groupby('Sub-Category')['Profit'].sum().min():,.0f} profit)."
)
st.markdown(
    f"- **Discount-profit correlation:** {disc_corr:.2f} — negative association "
    f"(descriptive, not causal)."
)
st.markdown(
    f"- **Loss-making orders:** {loss_orders} of {len(f)} rows "
    f"({loss_orders/len(f)*100:.1f}%)."
)

# --------------------------------------------------------------------------- #
# Data preview
# --------------------------------------------------------------------------- #
with st.expander("Data preview (first 10 rows)"):
    st.dataframe(f.head(10).reset_index(drop=True), use_container_width=True)

st.caption(
    "Data source: Superstore dataset (`Dataset/Sample - Superstore.csv`). "
    "Order ID does not uniquely identify a line item; order counts use unique Order IDs."
)
