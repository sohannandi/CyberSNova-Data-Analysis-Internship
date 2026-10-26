"""Shared data-loading utilities for CyberNova projects.

All helpers resolve paths relative to the repository root so that notebooks
and dashboards run from anywhere (``CyberNova/`` or a project folder).
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

# Repository layout constants.
# REPO_ROOT is the folder that contains the ``Dataset/`` directory. For the
# projects this is the ``CyberNova/`` checkout root.
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DATASET_DIR: Path = REPO_ROOT / "Dataset"


def get_repo_root() -> Path:
    """Return the repository root directory."""
    return REPO_ROOT


def resolve_repo_root() -> Path:
    """Resolve the repository root directory from the current working directory."""
    return REPO_ROOT


def get_dataset_path(filename: str) -> Path:
    """Return the absolute path to a file inside ``Dataset/``.

    Files are matched case-insensitively on Windows so callers need not
    worry about exact casing (the supplied files have mixed case).
    """
    for candidate in DATASET_DIR.iterdir():
        if candidate.name.lower() == filename.lower():
            return candidate
    return DATASET_DIR / filename


def resolve_project_root() -> Path:
    """Resolve the project root from the current working directory.

    Looks upward from the cwd for the folder that contains ``Dataset/``.
    Falls back to ``REPO_ROOT``.
    """
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "Dataset").is_dir() and (parent / "projects").is_dir():
            return parent
        if (parent / "Dataset").is_dir():
            return parent
    return REPO_ROOT


def load_csv(filename: str, parse_dates=None, encoding=None) -> pd.DataFrame:
    """Load a CSV from ``Dataset/`` with encoding fall-back handling.

    Parameters
    ----------
    filename:
        Name of the file inside ``Dataset/`` (matched case-insensitively).
    parse_dates:
        Passed through to ``pd.read_csv``.
    encoding:
        Optional encoding override. When ``None`` the file is decoded with
        UTF-8 first (``utf-8-sig`` handles a BOM) and falls back to
        ``latin-1`` which never fails for the supplied Western datasets.
    """
    path = get_dataset_path(filename)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {path}\n"
            f"Looked in: {DATASET_DIR}"
        )
    if encoding is not None:
        return pd.read_csv(path, parse_dates=parse_dates, encoding=encoding)

    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(path, parse_dates=parse_dates, encoding=enc)
        except UnicodeDecodeError:
            continue
    # Final fall-back (latin-1 never raises UnicodeDecodeError).
    return pd.read_csv(path, parse_dates=parse_dates, encoding="latin-1")


def df_summary(df: pd.DataFrame, name: str = "dataset") -> str:
    """Return a human-readable summary string of a DataFrame."""
    lines = [f"--- {name} ---",
             f"rows: {df.shape[0]}  cols: {df.shape[1]}",
             f"columns: {list(df.columns)}",
             "dtypes:"]
    lines.append(df.dtypes.astype(str).to_string())
    null_total = int(df.isnull().sum().sum())
    dup_total = int(df.duplicated().sum())
    lines.append(f"total nulls: {null_total}")
    lines.append(f"duplicate rows: {dup_total}")
    return "\n".join(lines)
