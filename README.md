# CMS Medical Equipment Supplier Acceptance Analysis

## Business Question
Which Medicare medical equipment suppliers are likely to accept assignment, and how accurately can a machine learning model predict that behavior?

## Headline Finding
The model correctly classifies 91% of suppliers. Predicted acceptance (53%) matches actual acceptance (51%) within 2 percentage points overall, and within 3 points in every risk tier — confirming strong aggregate and stratum-level calibration.

## Dataset
- **Source:** CMS Medical Equipment Suppliers  
  https://data.cms.gov/provider-data/dataset/ct36-nrcq
- **Scored:** 17 September 2026
- **Providers:** 56,898 (one row per provider, grain confirmed)
- **Target:** `acceptsassignment` (binary — accepts Medicare assignment)

## Pipeline
Seven notebooks, run in order:

| Notebook | Purpose |
|---|---|
| 01_data_quality | Schema audit, class balance, placeholder date flagging |
| 02_data_cleaning | Type coercion, date reliability scoring, null handling |
| 03_exploratory_analysis | Acceptance by state, specialty, and supply type |
| 04_feature_engineering | Specialty/supply dummies, tenure days, state encoding |
| 05_model_training | Five-model comparison; HistGradientBoostingClassifier selected |
| 06_model_evaluation | Threshold tuning, calibration check, confusion matrix |
| 07_powerbi_output | Scored export with Risk_Level, Prediction_Confidence, grain check |

## Model Selection
HistGradientBoostingClassifier chosen over five alternatives on **overfitting gap** (0.0101) rather than raw ROC-AUC — the model that generalizes best, not just the one that scores highest on training data.

**Classification threshold: 0.70**, validated at ~94.5% precision.

## Model Results

| Metric | Value |
|---|---|
| Accuracy | 91% |
| Precision | 89.9% |
| Recall | 92.7% |
| Calibration gap (aggregate) | 0.0pp |
| False positives | 3,094 |
| False negatives | 2,121 |

## Risk Tier Validation

Risk tiers derived from predicted probability with documented thresholds:

| Tier | Threshold | Providers | Predicted | Actual | Gap |
|---|---|---|---|---|---|
| Low Risk | ≥ 0.60 | 27,992 | 90% | 93% | +3pp |
| Medium Risk | 0.30–0.60 | 6,585 | 46% | 44% | −2pp |
| High Risk | < 0.30 | 22,620 | 5% | 3% | −2pp |

Tiers separate cleanly — 90 percentage points between Low and High — confirming the model's risk segmentation predicts real behavior.

## Key Findings
- **National acceptance rate: 51%.** The model predicts 53% — a 2-point gap.
- **Tier calibration holds at every level**, not just in aggregate.
- **88.5% of providers** fall in Low or High Risk tiers where the model predicts with high confidence. Only 11.5% fall in the uncertain Medium tier.
- **Regional variation:** Upper Midwest and Northeast show the highest acceptance rates; Southwest and Southeast the lowest.
- **Specialty variation:** Pharmacy and Optician show strong acceptance; Orthotic Personnel and Medical Supply Company Other show weaker engagement.

## Data Quality Notes
- ~5,400 records carry suspected placeholder enrollment dates (`date_reliability_flag`). Excluded from enrollment cohort analysis but retained for model scoring.
- Specialty and supply type are pipe-delimited multi-value fields. Bridge tables (ProviderSpecialties, ProviderSupplies) handle the many-to-many relationship without duplicating fact rows.
- **Leakage review:** two alternative CSV versions were rejected after identifying data leakage. The pipeline runs on the clean extract only.

## Dashboard
Built in Power BI against a star schema:
`Fact_Providers` → `DimSpecialties`, `DimSupplies`, `ProviderSpecialties` (bridge), `ProviderSupplies` (bridge)

Visuals: KPI cards · Risk-tier table · Confusion matrix · Specialty scatter (predicted vs actual, ratio line) · State choropleth · Bottom-10 states bar chart

## Roadmap
- **Time-series analysis** requires multi-period CMS extracts. Snapshot archiving began September 2026; quarterly pulls will enable genuine YoY comparison by late 2027.
- **Automated refresh** would require scheduled pipeline execution (Airflow or Azure Data Factory) with a Power BI Gateway. Current scope is manual re-scoring.
- **Regional driver analysis** — acceptance rate varies substantially by state. Identifying whether policy, market structure, or supplier mix drives the pattern requires additional data.

## Repository Structure
cms-supplier-acceptance-analysis/
├── data/
│ ├── raw/ # CMS extracts (gitignored)
│ └── processed/ # Scored output (gitignored)
├── models/trained/ # Saved .joblib model
├── notebooks/ # 01–07 pipeline
├── reports/figures/ # EDA and evaluation charts
└── README.md