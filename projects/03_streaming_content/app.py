"""Movie Streaming Platform Analysis - Interactive Streamlit Dashboard."""

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
    src = DATASET_DIR / "netflix_titles.csv"
    assert src.exists(), f"Dataset file not found: {src}"
    df = pd.read_csv(src, encoding="utf-8")
    # quick clean for charts
    df["country_clean"] = df["country"].astype(str).str.strip()
    df["listed_in_clean"] = df["listed_in"].astype(str).str.strip()
    df["duration_num"] = df["duration"].apply(
        lambda x: float(str(x).replace(" min", "").replace(" Seasons", "").replace(" Season", ""))
        if (" min" in str(x) or "Season" in str(x)) and str(x).replace(" min","").replace(" Seasons","").replace(" Season","").replace(".","").isdigit()
        else np.nan
    )
    df["duration_unit"] = df["duration"].apply(
        lambda x: "minutes" if str(x).strip().endswith(" min") else
        ("seasons" if str(x).strip().endswith(" Seasons") or str(x).strip().endswith(" Season") else np.nan)
    )
    return df


st.set_page_config(page_title="Streaming Content Dashboard", layout="wide")

st.title("🎬 Movie Streaming Platform Dashboard")
st.markdown(
    "**Level:** Beginner  |  **Dataset:** `Dataset/netflix_titles.csv`  "
    "|  **Intern:** Sohan Nandi (CSN-OC-2026-474)  |  **October 2026**"
)
st.caption(
    "Explore movie vs TV-show catalog composition, release-year trends, genres, countries, and duration patterns. "
    "Missing descriptive fields are treated as missing; never imputed."
)
st.markdown("---")

df = load_data()
clean = df.copy()
clean.to_csv(OUT_DIR / "cleaned_streaming_content.csv", index=False)

# --------------------------------------------------------------------------- #
# Filters
# --------------------------------------------------------------------------- #
st.sidebar.header("Filters")
type_sel = st.sidebar.multiselect(
    "Type", options=sorted(clean["type"].unique()), default=sorted(clean["type"].unique())
)
year_sel = st.sidebar.multiselect(
    "Release Year", options=sorted(clean["release_year"].dropna().unique()),
    default=sorted(clean["release_year"].dropna().unique())
)
rating_sel = st.sidebar.multiselect(
    "Rating", options=sorted(clean["rating"].dropna().unique()), default=sorted(clean["rating"].dropna().unique())
)
country_sel = st.sidebar.multiselect(
    "Country", options=sorted(clean["country_clean"].dropna().unique()),
    default=sorted(clean["country_clean"].dropna().unique())[:20]  # limit for UI
)
genre_sel = st.sidebar.multiselect(
    "Genre", options=sorted(clean["listed_in_clean"].dropna().unique()),
    default=sorted(clean["listed_in_clean"].dropna().unique())[:15]
)

f = clean
if type_sel:
    f = f[f["type"].isin(type_sel)]
if year_sel:
    f = f[f["release_year"].isin(year_sel)]
if rating_sel:
    f = f[f["rating"].isin(rating_sel)]
if country_sel:
    f = f[f["country_clean"].isin(country_sel)]
if genre_sel:
    f = f[f["listed_in_clean"].isin(genre_sel)]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# --------------------------------------------------------------------------- #
# KPIs
# --------------------------------------------------------------------------- #
st.subheader("Key Metrics")
c1, c2, c3 = st.columns(3)
c1.metric("Titles", f"{len(f):,}")
c2.metric("Movies", f"{(f['type']=='Movie').sum():,}")
c3.metric("TV Shows", f"{(f['type']=='TV Show').sum():,}")
c4, c5 = st.columns(2)
c4.metric("Distinct Years", f"{f['release_year'].nunique()}")
c5.metric("Distinct Ratings", f"{f['rating'].notna().sum()}")

# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
st.subheader("Title Type & Release Trends")
c1, c2 = st.columns(2)
with c1:
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    f["type"].value_counts().plot(kind="bar", ax=ax1, color=["#1f77b4", "#ff7f0e"])
    ax1.set_title("Title Type Distribution")
    ax1.set_ylabel("Count")
    ax1.tick_params(axis="x", rotation=0)
    st.pyplot(fig1, use_container_width=True)
with c2:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    rel = f["release_year"].value_counts().sort_index()
    if not rel.empty:
        rel.plot(kind="line", marker="o", ax=ax2, color="#2ca02c")
        ax2.set_title("Releases by Release Year")
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Count")
        ax2.tick_params(axis="x", rotation=45)
    st.pyplot(fig2, use_container_width=True)

st.subheader("Top Genres & Countries")
c1, c2 = st.columns(2)
with c1:
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    genres = f["listed_in_clean"].dropna().astype(str).str.split(",").explode().str.strip()
    gv = genres.value_counts().head(10)
    if not gv.empty:
        gv.plot(kind="barh", ax=ax3, color="#9467bd")
        ax3.set_title("Top Genres (may appear in multiple)")
        ax3.set_xlabel("Count")
    st.pyplot(fig3, use_container_width=True)
with c2:
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    countries = f["country_clean"].dropna().astype(str).str.split(",").explode().str.strip()
    cv = countries.value_counts().head(10)
    if not cv.empty:
        cv.plot(kind="barh", ax=ax4, color="#8c564b")
        ax4.set_title("Top Countries")
        ax4.set_xlabel("Count")
    st.pyplot(fig4, use_container_width=True)

st.subheader("Rating Distribution & Duration")
c1, c2 = st.columns(2)
with c1:
    fig5, ax5 = plt.subplots(figsize=(7, 4))
    f["rating"].value_counts().head(10).plot(kind="bar", ax=ax5, color="#d62728")
    ax5.set_title("Rating Distribution")
    ax5.set_ylabel("Count")
    ax5.tick_params(axis="x", rotation=45)
    st.pyplot(fig5, use_container_width=True)
with c2:
    fig6, ax6 = plt.subplots(figsize=(7, 4))
    min_d = f[f["duration_unit"]=="minutes"]["duration_num"].dropna()
    if not min_d.empty:
        min_d.plot(kind="hist", bins=20, ax=ax6, color="#e377c2", edgecolor="white")
        ax6.set_title("Movie Duration (minutes)")
        ax6.set_xlabel("Minutes")
    else:
        ax6.text(0.5, 0.5, "No movie minutes data", ha="center", va="center")
        ax6.set_title("Movie Duration")
    st.pyplot(fig6, use_container_width=True)

st.subheader("Duration: Movies vs TV Shows")
fig7, ax7 = plt.subplots(figsize=(8, 4))
sea_d = f[f["duration_unit"]=="seasons"]["duration_num"].dropna()
if not min_d.empty and not sea_d.empty:
    # side-by-side histograms for comparison
    bins = np.linspace(0, max(min_d.max(), sea_d.max())+1, 15)
    ax7.hist(min_d, bins=bins, alpha=0.5, label="Movie minutes", color="#1f77b4")
    ax7.hist(sea_d, bins=bins, alpha=0.5, label="TV seasons", color="#ff7f0e")
    ax7.set_title("Duration Distributions — Movies vs TV (NOT directly comparable units)")
    ax7.set_xlabel("Minutes / Seasons")
    ax7.legend()
    st.pyplot(fig7, use_container_width=True)
else:
    ax7.text(0.5, 0.5, "Insufficient duration data", ha="center", va="center")
    ax7.set_title("Duration")
    st.pyplot(fig7, use_container_width=True)

# --------------------------------------------------------------------------- #
# Key findings
# --------------------------------------------------------------------------- #
st.markdown("---")
st.subheader("Key Findings")
top_country = f["country_clean"].dropna().astype(str).str.split(",").explode().str.strip().value_counts().idxmax() if not f.empty else "N/A"
top_genre = f["listed_in_clean"].dropna().astype(str).str.split(",").explode().str.strip().value_counts().idxmax() if not f.empty else "N/A"
n_movies = (f["type"]=="Movie").sum()
n_tv = (f["type"]=="TV Show").sum()
n_yr = f["release_year"].nunique()
rating_top = f["rating"].value_counts().idxmax() if not f.empty else "N/A"

st.markdown(
    f"- **Catalog split:** Movies {n_movies:,} ({n_movies/len(f)*100:.1f}%) | TV Shows {n_tv:,} ({n_tv/len(f)*100:.1f}%)."
)
st.markdown(
    f"- **Top country:** {top_country} ({f['country_clean'].dropna().astype(str).str.split(',').explode().str.strip().value_counts().iloc[0]} titles)."
)
st.markdown(
    f"- **Top genre:** {top_genre}."
)
st.markdown(
    f"- **Release-year span:** {f['release_year'].min()} to {f['release_year'].max()} ({n_yr} distinct years)."
)
st.markdown(
    f"- **Most common rating:** {rating_top} ({f['rating'].value_counts().iloc[0]} titles)."
)
st.markdown(
    f"- **Movie minutes vs TV seasons** are kept on separate scales; direct comparison is misleading."
)
st.markdown(
    f"- Missing descriptive fields (director, cast, country, rating) are never imputed; treated as missing data."
)

with st.expander("Data preview (first 10 rows)"):
    st.dataframe(f.head(10).reset_index(drop=True), use_container_width=True)

st.caption(
    "Data source: Netflix titles dataset (`Dataset/netflix_titles.csv`). "
    "Missing fields are treated as missing; comma-separated country/genre fields "
    "mean one title may appear in multiple categories. Movie minutes vs TV seasons "
    "are NOT directly comparable."
)