# Data and Model Limitations

| Limitation | Impact | How it is handled |
|---|---|---|
| **Single snapshot.** One CMS extract (September 2026). | No trend or year-over-year analysis. Enrollment year describes when a provider joined, not a timeline. | Trend analysis is out of scope. The pipeline can be re-run on future extracts. |
| **Suspected placeholder dates.** 5,390 providers have a participation start date matching one of the 10 most common pre-2000 dates (for example, 3,959 share 1998-01-01). | Tenure is unreliable for those providers. | Flagged rather than deleted (`is_suspected_placeholder_date`). The leakage review in Notebook 06 found the flag has negligible importance. |
| **Directory data, not claims data.** | Shows whether a supplier *states* it accepts assignment, not how it actually bills. | Findings are described as directory-level. |
| **Predictions include training rows.** The export scores all 56,898 providers, 45,518 of which the model was trained on. | In-sample metrics look better than they are (90.9% vs 89.8% accuracy at 0.50). | All model metrics in the dashboard use the 11,380 held-out test providers only. |
| **Top feature is a cohort effect, not a trend.** `tenure_days` ranks #1 in permutation importance, but acceptance is ~39–46% in most tenure bands and 96% only for providers enrolled roughly late 2020 to early 2023 (Spearman ρ = −0.08, training data). | "Longer tenure → higher acceptance" would be misleading. The cause of the cohort effect (policy change or supplier mix) is unknown. | Reported as an enrollment-cohort hypothesis to test with multi-year extracts (Notebook 06). |
| **Observational model.** | Feature importance shows association, not cause. | Wording throughout is associational (no "drives" or "causes"). |
| **Multi-value specialties and supplies.** One provider can list several. | One provider counts in several categories, so category totals exceed the provider total. | Bridge tables in Power BI keep the one-row-per-provider grain. |
| **Imputed categoricals.** A small number of missing category values were filled during cleaning. | Small bias risk in those columns. | Every cleaning decision is logged in `reports/validation/data_cleaning_log.csv`. |
| **Case 2 threshold (0.70).** | Higher precision (94.8%) at the cost of recall (81.6%). False positives average a predicted probability of 0.67, close to the threshold. | Case 2 results are presented as high-likelihood candidates, not confirmed outcomes. |
