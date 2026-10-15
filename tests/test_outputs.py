"""Data-quality checks on the pipeline outputs.

Run from the project root:  python -m pytest -v
Tests are skipped if the processed data is not present
(data/ is git-ignored, so run Notebooks 01-07 first).
"""
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
PRED_PATH = ROOT / "data" / "processed" / "cms_supplier_predictions.csv"

EXPECTED_TOTAL = 56_898
EXPECTED_TRAIN = 45_518
EXPECTED_TEST = 11_380


@pytest.fixture(scope="module")
def preds():
    if not PRED_PATH.exists():
        pytest.skip(f"{PRED_PATH} not found - run the notebooks first")
    return pd.read_csv(PRED_PATH)


def _actual_as_int(df):
    """Actual_Acceptance_Bool may be saved as True/False or 1/0."""
    mapping = {True: 1, False: 0, "True": 1, "False": 0, 1: 1, 0: 0}
    return df["Actual_Acceptance_Bool"].map(mapping)


def test_row_count(preds):
    assert len(preds) == EXPECTED_TOTAL


def test_provider_id_unique(preds):
    assert preds["provider_id"].is_unique


def test_no_missing_key_fields(preds):
    cols = ["provider_id", "Predicted_Probability", "Actual_Acceptance_Bool", "split"]
    assert preds[cols].notna().all().all()


def test_probabilities_between_0_and_1(preds):
    p = preds["Predicted_Probability"]
    assert p.between(0, 1).all()


def test_split_sizes(preds):
    counts = preds["split"].value_counts()
    assert counts["train"] == EXPECTED_TRAIN
    assert counts["test"] == EXPECTED_TEST
    assert counts["train"] + counts["test"] == EXPECTED_TOTAL


def test_actual_label_is_binary(preds):
    y = _actual_as_int(preds)
    assert y.notna().all()
    assert set(y.unique()) <= {0, 1}


def test_overall_acceptance_rate(preds):
    rate = _actual_as_int(preds).mean()
    assert round(rate, 3) == 0.513


def test_test_set_accuracy_matches_reported(preds):
    test = preds[preds["split"] == "test"]
    y = _actual_as_int(test)
    pred = (test["Predicted_Probability"] >= 0.5).astype(int)
    accuracy = (pred == y).mean()
    # Reported in the dashboard and model card: 89.8%
    assert round(accuracy, 3) == 0.898