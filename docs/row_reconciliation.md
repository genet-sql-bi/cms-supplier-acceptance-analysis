# Row Reconciliation

Every stage of the pipeline was checked to confirm that no providers are lost or duplicated between the raw CMS extract and the Power BI dashboard.

**Source:** CMS Medical Equipment Suppliers, September 2026 extract
(`data/raw/Medical-Equipment-Suppliers_2026-09.csv`)

## Row counts by stage

| Stage | Output | Rows | Distinct `provider_id` | Notes |
|---|---|---|---|---|
| Raw extract | `data/raw/Medical-Equipment-Suppliers_2026-09.csv` | 56,898 | 56,898 | 17 columns |
| 02 Cleaning | `data/interim/cms_suppliers_cleaned.csv` | 56,898 | 56,898 | 0 rows removed; 17 → 13 columns |
| 04 Feature engineering | `data/interim/model_features_full.csv` | 56,898 | 56,898 | 165 model features |
| 04 Train/test split | `X_train.csv` / `X_test.csv` | 45,518 / 11,380 | — | 80/20, stratified, `random_state=42` |
| 07 Power BI export | `data/processed/cms_supplier_predictions.csv` | 56,898 | 56,898 | Grain check: PASS |
| Power BI | `Fact_Providers` | 56,898 | 56,898 | Total Providers card |

The row count is unchanged at every stage: one row per provider, from raw data to dashboard.

## Train/test membership

`data/processed/train_test_split.csv` records whether each provider was in the training or test set. The split is rebuilt in Notebook 07 from the same target, test size and seed as Notebook 04, then verified row by row against the saved `X_test.csv` and `y_test.csv`. The notebook stops with an error if they do not match.

All model performance figures in the dashboard are filtered to the 11,380 **test** providers. Power BI and Python agree exactly:

| Threshold | TP | FP | FN | TN | Accuracy | Precision | Recall |
|---|---|---|---|---|---|---|---|
| 0.50 | 5,353 | 671 | 485 | 4,871 | 89.8% | 88.9% | 91.7% |
| 0.70 | 4,765 | 263 | 1,073 | 5,279 | 88.3% | 94.8% | 81.6% |

## Earlier extract (reference only)

An earlier July 2026 extract (`data/raw/Medical-Equipment-Suppliers_2026-07.csv`) contained 57,197 rows. The pipeline was re-run end to end on the September extract, and all reported figures come from that run. The July file is kept only for reference and is not used by any notebook.
