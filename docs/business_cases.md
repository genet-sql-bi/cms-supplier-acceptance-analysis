# Business Cases

**Data:** CMS Medical Equipment Supplier directory, September 2026 snapshot. **56,898 providers**, of which **29,191 accept** assignment and **27,707 do not** (51.3%).
**Model:** HistGradientBoosting classifier. Performance is measured on the **held-out test set (n = 11,380)**, i.e. providers the model never saw during training.

Every number below was verified in the re-run pipeline (Notebooks 01–07) and/or the Power BI test-set check. The only exceptions are the **ROI assumptions (marked 💲)**, which are business assumptions, not findings.

**ROI formula:** ROI = (Annual gain − Cost) ÷ Cost

---

## Case 1: Raise acceptance where it is lowest

### Objective
Increase Medicare assignment acceptance among the **27,707 providers who do not currently accept**, starting with the **states and provider types with the lowest acceptance**. Use the model's predicted probability to prioritise who to contact.

### Positive insight
High acceptance is achievable. **Optometrists accept at 94.7%**, against **51.3% nationally**. That's **43.4 points higher**, a **85% relative lift** ((94.7 − 51.3) ÷ 51.3). The practices of high-acceptance provider types can serve as the playbook for outreach.

### Negative insight
Acceptance is lowest in specific places and provider types:
- **Hawaii has the lowest acceptance of any state at 37.9%** (states with at least 100 providers), **13.4 points below** the national rate.
- **Opticians accept at only 22.6%**, less than half the national rate.
- **Alabama:** of **1,008 providers, only 455 accept (45.1%)**, leaving **553 who don't**.

Nationally, nearly half of all providers (**27,707 of 56,898**) do not accept assignment, so their patients face higher out-of-pocket costs.

### ROI 💲
| Item | Value |
|---|---|
| Target group | 27,707 non-accepting providers (verified) |
| Conversion from outreach 💲 | 5% → **1,385 providers** |
| Annual value per newly accepting provider 💲 | $1,200 |
| Annual gain | 1,385 × $1,200 = **$1,662,000** |
| Outreach cost (3 months) 💲 | $270,000 |
| **ROI** | (1,662,000 − 270,000) ÷ 270,000 = **≈ 516%** |

---

## Case 2: Convert providers the model expects to accept but who don't

### Objective
Target providers with a **predicted probability of accepting of at least 0.70** who **do not currently accept**. They closely resemble acceptors, so they should be the easiest to convert.

### Positive insight
At the 0.70 threshold, the model is highly reliable. Of the **5,028 test-set providers it flagged**, **4,765 really accept**, giving **94.8% precision**. That compares with **51.3% acceptance** across the whole test set: providers the model flags are **1.85 times more likely to accept** than average.

### Negative insight
Even so, **263 flagged providers (5.2%) do not accept**, despite looking like acceptors. Their average predicted probability is **0.67**, close to the threshold. Scaled from the test set to the whole directory, that's **about 1,315 providers** (263 ÷ 11,380 × 56,898), a group with high acceptance potential that is currently missed revenue and missed patient access.

### ROI 💲
| Item | Value |
|---|---|
| Target group | ≈ 1,315 providers (estimate scaled from the test set) |
| Conversion (higher; they already resemble acceptors) 💲 | 25% → **329 providers** |
| Annual value per newly accepting provider 💲 | $1,200 |
| Annual gain | 329 × $1,200 = **$394,800** |
| Engagement cost (2 months, light-touch) 💲 | $100,000 |
| **ROI** | (394,800 − 100,000) ÷ 100,000 = **≈ 295%** |

---

## Executive summary (50 words)
Case 1 targets the 27,707 providers not accepting assignment, prioritising the lowest-acceptance areas (Hawaii 37.9%, Opticians 22.6%). It's the larger opportunity ($1.66M, ≈516% ROI). Case 2 converts about 1,315 providers the model flags as likely acceptors, which is cheaper and more certain ($395K, ≈295% ROI). The choice depends on budget and timeline.

---

## Source of every number
| Number | Source |
|---|---|
| 56,898 providers; 29,191 accept / 27,707 do not; 51.3% | Notebooks 01–03 (September extract) |
| Hawaii 37.9%; Alabama 1,008 / 455 / 45.1%; Opticians 22.6%; Optometrists 94.7% | Notebook 03, `eda_key_findings.csv` |
| Test set 11,380; TP 4,765; FP 263; precision 94.8% at 0.70 | Notebook 07 and Power BI (match exactly) |
| False-positive average probability 0.67 | Notebook 06, `model_card.json` |
| ≈ 1,315 providers | Calculated: 263 ÷ 11,380 × 56,898 (an estimate) |
| Conversion rates, $1,200 per provider, costs | 💲 Business assumptions, adjust as needed |

**Not used, because the current data contradicts them:** the earlier project's "Alabama 195 providers / 1% acceptance" (the real figure is 1,008 / 45.1%), and "predicted 99% vs actual 34%" (the real precision at 0.70 is 94.8%).