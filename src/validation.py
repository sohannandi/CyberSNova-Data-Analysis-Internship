"""Reusable data-validation helpers used by the project tests and notebooks.

Each validator raises ``ValidationError`` with a clear message when the
precondition is not met, so notebooks/tests can surface the problem instead
of silently failing downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import pandas as pd


class ValidationError(Exception):
    """Raised when a data-quality precondition is not satisfied."""


# Expected schema: project -> (filename, set of required columns).
# These are the *actual* columns present in the supplied CSVs.
EXPECTED_SCHEMA: dict[str, tuple[str, list[str]]] = {
    "retail_sales": (
        "Sample - Superstore.csv",
        ["Row ID", "Order ID", "Order Date", "Ship Date", "Customer ID",
         "Customer Name", "Segment", "Country", "State", "Postal Code",
         "Region", "Category", "Sub-Category", "Product Name", "Sales",
         "Quantity", "Discount", "Profit"],
    ),
    "student_performance": (
        "StudentsPerformance.csv",
        ["gender", "race/ethnicity", "parental level of education", "lunch",
         "test preparation course", "math score", "reading score",
         "writing score"],
    ),
    "streaming_content": (
        "netflix_titles.csv",
        ["show_id", "type", "title", "director", "cast", "country",
         "date_added", "release_year", "rating", "duration", "listed_in",
         "description"],
    ),
    "telecom_churn": (
        "WA_Fn-UseC_-Telco-Customer-Churn.csv",
        ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
         "tenure", "PhoneService", "MultipleLines", "InternetService",
         "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
         "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
         "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"],
    ),
    "hr_analytics": (
        "HR_comma_sep.csv",
        ["satisfaction_level", "last_evaluation", "number_project",
         "average_montly_hours", "time_spend_company", "Work_accident",
         "left", "promotion_last_5years", "Department", "salary"],
    ),
}


@dataclass
class ValidationResult:
    """Structured result of a validation run."""
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        msg = "PASS" if self.ok else "FAIL"
        parts = []
        if self.errors:
            parts.append("errors:\n" + "\n".join(f"  - {e}" for e in self.errors))
        if self.warnings:
            parts.append("warnings:\n" + "\n".join(f"  - {w}" for w in self.warnings))
        if parts:
            msg += " | " + " | ".join(parts)
        return msg


def assert_columns(df: pd.DataFrame, required: Iterable[str],
                   context: str = "dataset") -> None:
    """Raise ``ValidationError`` if any *required* columns are missing."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValidationError(
            f"{context} is missing required columns: {missing}.\n"
            f"Found columns: {list(df.columns)}"
        )


def assert_file_exists(path: Path) -> None:
    """Raise ``ValidationError`` (wrapping FileNotFoundError) if *path* is absent."""
    if not path.exists():
        raise ValidationError(f"Required source file not found: {path}")


def check_dtypes(df: pd.DataFrame, expected: dict[str, str]) -> list[str]:
    """Return a list of human-readable mismatches for numeric/string columns."""
    warnings = []
    for col, kind in expected.items():
        if col not in df.columns:
            continue
        if kind == "numeric" and not pd.api.types.is_numeric_dtype(df[col]):
            warnings.append(f"column '{col}' expected numeric, got {df[col].dtype}")
        elif kind == "string" and pd.api.types.is_numeric_dtype(df[col]):
            warnings.append(f"column '{col}' expected string/object, got {df[col].dtype}")
    return warnings
