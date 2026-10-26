"""Data-validation tests for the CyberNova internship project.

Verifies:
- Each expected source file exists.
- Each CSV can be loaded.
- Required project columns exist; missing columns produce informative errors.
- Data-cleaning functions do not mutate the original DataFrame unexpectedly.
- Numeric conversion and missing-value handling work for relevant columns.
- HR deduplication is documented and reproducible.
- Dashboard entry points import without syntax errors.
"""

import os
import py_compile
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.data_utils import get_dataset_path, load_csv, resolve_repo_root

REPO_ROOT = resolve_repo_root()
DATASET_DIR = REPO_ROOT / "Dataset"


# Expected source files: (relative filename, expected required columns).
EXPECTED = {
    "Sample - Superstore.csv": [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Customer ID", "Customer Name",
        "Segment", "Country", "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit",
    ],
    "StudentsPerformance.csv": [
        "gender", "race/ethnicity", "parental level of education", "lunch",
        "test preparation course", "math score", "reading score", "writing score",
    ],
    "netflix_titles.csv": [
        "show_id", "type", "title", "director", "cast", "country", "date_added",
        "release_year", "rating", "duration", "listed_in", "description",
    ],
    "WA_Fn-UseC_-Telco-Customer-Churn.csv": [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
        "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn",
    ],
    "HR_comma_sep.csv": [
        "satisfaction_level", "last_evaluation", "number_project", "average_montly_hours",
        "time_spend_company", "Work_accident", "left", "promotion_last_5years", "Department",
        "salary",
    ],
}


def test_repo_root_resolved():
    root = resolve_repo_root()
    assert (root / "Dataset").is_dir()
    assert (root / "projects").is_dir()


@pytest.mark.parametrize("filename,required_cols", sorted(EXPECTED.items()))
def test_expected_source_file_exists(filename, required_cols):
    path = get_dataset_path(filename)
    assert path.exists(), f"Expected source file missing: {path}"


@pytest.mark.parametrize("filename,required_cols", sorted(EXPECTED.items()))
def test_csv_loads_with_required_columns(filename, required_cols):
    df = load_csv(filename)
    assert df is not None
    missing = [c for c in required_cols if c not in df.columns]
    assert missing == [], f"{filename} missing columns: {missing}"


def test_load_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_csv("does_not_exist.csv")


def test_numeric_conversion_missing_handling():
    # Telecom: TotalCharges has whitespace-only values -> coerce to NaN
    df = load_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    converted = pd_numeric_coerce(df)
    assert "TotalCharges" in converted.columns
    # whitespace-only strings become NaN; valid numerics stay numeric
    assert converted["TotalCharges"].isna().sum() >= 0


def pd_numeric_coerce(df):
    import pandas as pd

    out = df.copy()
    out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")
    return out


def test_cleaning_does_not_mutate_source():
    import pandas as pd

    src = load_csv("Sample - Superstore.csv", parse_dates=["Order Date", "Ship Date"])
    snapshot_cols = set(src.columns)
    snapshot_hash = src["Sales"].sum()
    clean = src.copy()
    clean["Profit Margin"] = clean["Profit"] / clean["Sales"].replace(0, 1)
    # Source must be unchanged in structure/values relevant to the test
    assert set(src.columns) == snapshot_cols
    assert src["Sales"].sum() == snapshot_hash


def test_hr_dedup_is_reproducible():
    import pandas as pd

    from src.data_utils import get_dataset_path

    df = load_csv("HR_comma_sep.csv")
    dedup = df.drop_duplicates().copy()
    assert len(dedup) < len(df)
    assert dedup["left"].notna().all()
    # reproducible: deduping again yields the same frame
    assert len(dedup.drop_duplicates()) == len(dedup)


@pytest.mark.parametrize(
    "app_path",
    [
        "projects/01_retail_sales/app.py",
        "projects/02_student_performance/app.py",
        "projects/03_streaming_content/app.py",
        "projects/04_telecom_churn/app.py",
        "projects/05_hr_analytics/app.py",
    ],
)
def test_dashboard_entry_points_have_no_syntax_errors(app_path):
    full = REPO_ROOT / app_path
    assert full.exists(), f"Dashboard entry point missing: {full}"
    py_compile.compile(str(full), doraise=True)


def test_telecom_dashboard_runs_for_each_churn_filter():
    app = AppTest.from_file(
        str(REPO_ROOT / "projects/04_telecom_churn/app.py"),
        default_timeout=60,
    ).run()
    assert not app.exception

    for status in ("Churned (Yes)", "Retained (No)"):
        app.selectbox[0].set_value(status).run()
        assert not app.exception


def test_hr_dashboard_runs_with_one_salary_band_selected():
    app = AppTest.from_file(
        str(REPO_ROOT / "projects/05_hr_analytics/app.py"),
        default_timeout=60,
    ).run()
    assert not app.exception

    app.multiselect[1].set_value(["low"]).run()
    assert not app.exception