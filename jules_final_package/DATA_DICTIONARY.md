# Data and results dictionary

Generated from the files themselves: row counts, header rows and first/last keys are read from disk. Paths are relative to the repository root.

## `data/`

### `data/gate10/calibration/da_price_baseline_forecasts.csv`  (925.3 KiB)

Rows (excluding header): 15,335  |  Columns: 6

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:00:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `da_price_eur_mwh` | SMARD DE-LU day-ahead price, EUR/MWh |
| `period` | sample period label of the calibration set |
| `forecast_lag24` | day-ahead price forecast, 24 h lag persistence, EUR/MWh |
| `forecast_lag168` | day-ahead price forecast, 168 h lag persistence, EUR/MWh |
| `forecast_hybrid` | blended forecast used by the bidding model, EUR/MWh |

### `data/gate10/calibration/da_price_calibrated_forecast.csv`  (1786.4 KiB)

Rows (excluding header): 15,335  |  Columns: 9

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:00:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `period` | sample period label of the calibration set |
| `da_price_eur_mwh` | SMARD DE-LU day-ahead price, EUR/MWh |
| `forecast_hybrid` | blended forecast used by the bidding model, EUR/MWh |
| `price_error` | realized minus forecast, EUR/MWh |
| `lower_90` | 10th percentile of the forecast-error distribution, EUR/MWh |
| `upper_90` | 90th percentile of the forecast-error distribution, EUR/MWh |
| `lower_95` | 2.5th percentile of the forecast-error distribution, EUR/MWh |
| `upper_95` | 97.5th percentile of the forecast-error distribution, EUR/MWh |

### `data/gate10/calibration/joint_residual_correlation.csv`  (0.6 KiB)

Rows (excluding header): 5  |  Columns: 6

Square matrix (first column is the row index).

| Column | Meaning |
|---|---|
| `(index)` | project-specific; read by the scripts in `scripts/` |
| `price_error` | realized minus forecast, EUR/MWh |
| `load_error` | load forecast residual, standardized |
| `wind_on_error` | onshore-wind forecast residual, standardized |
| `wind_off_error` | offshore-wind forecast residual, standardized |
| `pv_error` | PV forecast residual, standardized |

### `data/gate10/calibration/joint_residual_database_hourly.csv`  (1259.1 KiB)

Rows (excluding header): 15,335  |  Columns: 7

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:00:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `period` | sample period label of the calibration set |
| `price_error` | realized minus forecast, EUR/MWh |
| `load_error` | load forecast residual, standardized |
| `wind_on_error` | onshore-wind forecast residual, standardized |
| `wind_off_error` | offshore-wind forecast residual, standardized |
| `pv_error` | PV forecast residual, standardized |

### `data/gate10/calibration/student_t_copula_correlation.csv`  (0.6 KiB)

Rows (excluding header): 5  |  Columns: 6

Square matrix (first column is the row index).

| Column | Meaning |
|---|---|
| `(index)` | project-specific; read by the scripts in `scripts/` |
| `price_error` | realized minus forecast, EUR/MWh |
| `load_error` | load forecast residual, standardized |
| `wind_on_error` | onshore-wind forecast residual, standardized |
| `wind_off_error` | offshore-wind forecast residual, standardized |
| `pv_error` | PV forecast residual, standardized |

### `data/gate10/calibration/student_t_copula_correlation_bias_corrected.csv`  (0.5 KiB)

Rows (excluding header): 5  |  Columns: 6

Square matrix (first column is the row index).

| Column | Meaning |
|---|---|
| `(index)` | project-specific; read by the scripts in `scripts/` |
| `price_error` | realized minus forecast, EUR/MWh |
| `load_error` | load forecast residual, standardized |
| `wind_on_error` | onshore-wind forecast residual, standardized |
| `wind_off_error` | offshore-wind forecast residual, standardized |
| `pv_error` | PV forecast residual, standardized |

### `data/gate10/processed/load_forecast_derived_from_smard.csv`  (3771.6 KiB)

Rows (excluding header): 61,340  |  Columns: 6

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:45:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `load_forecast` | project-specific; read by the scripts in `scripts/` |
| `residual_load_forecast` | project-specific; read by the scripts in `scripts/` |
| `wind_on_forecast` | project-specific; read by the scripts in `scripts/` |
| `wind_off_forecast` | project-specific; read by the scripts in `scripts/` |
| `pv_forecast` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/processed/master_da_price_hourly.csv`  (496.2 KiB)

Rows (excluding header): 15,335  |  Columns: 2

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:00:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `da_price_eur_mwh` | SMARD DE-LU day-ahead price, EUR/MWh |

### `data/gate10/processed/master_information_set.csv`  (13642.7 KiB)

Rows (excluding header): 61,340  |  Columns: 19

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:45:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `load_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_on_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_off_actual` | project-specific; read by the scripts in `scripts/` |
| `pv_actual` | project-specific; read by the scripts in `scripts/` |
| `residual_load_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_on_forecast` | project-specific; read by the scripts in `scripts/` |
| `wind_off_forecast` | project-specific; read by the scripts in `scripts/` |
| `pv_forecast` | project-specific; read by the scripts in `scripts/` |
| `residual_load_calculated` | project-specific; read by the scripts in `scripts/` |
| `residual_load_error` | project-specific; read by the scripts in `scripts/` |
| `delivery_date` | project-specific; read by the scripts in `scripts/` |
| `da_decision_time` | project-specific; read by the scripts in `scripts/` |
| `renewable_forecast_available_by` | project-specific; read by the scripts in `scripts/` |
| `load_forecast_available_by` | project-specific; read by the scripts in `scripts/` |
| `wind_forecast_DA_eligible` | project-specific; read by the scripts in `scripts/` |
| `wind_off_forecast_DA_eligible` | project-specific; read by the scripts in `scripts/` |
| `pv_forecast_DA_eligible` | project-specific; read by the scripts in `scripts/` |
| `load_forecast_DA_eligible` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/processed/master_physical_15min.csv`  (6065.6 KiB)

Rows (excluding header): 61,340  |  Columns: 11

Range on `timestamp`: `2024-01-01 00:00:00+01:00` → `2025-09-30 23:45:00+02:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `load_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_on_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_off_actual` | project-specific; read by the scripts in `scripts/` |
| `pv_actual` | project-specific; read by the scripts in `scripts/` |
| `residual_load_actual` | project-specific; read by the scripts in `scripts/` |
| `wind_on_forecast` | project-specific; read by the scripts in `scripts/` |
| `wind_off_forecast` | project-specific; read by the scripts in `scripts/` |
| `pv_forecast` | project-specific; read by the scripts in `scripts/` |
| `residual_load_calculated` | project-specific; read by the scripts in `scripts/` |
| `residual_load_error` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/reduction_diagnostics_100.csv`  (0.3 KiB)

Rows (excluding header): 5  |  Columns: 3

Range on `variable`: `price_error_bc` → `pv_error_bc`

| Column | Meaning |
|---|---|
| `variable` | project-specific; read by the scripts in `scripts/` |
| `mean_error` | project-specific; read by the scripts in `scripts/` |
| `std_error` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/reduction_diagnostics_30.csv`  (0.3 KiB)

Rows (excluding header): 5  |  Columns: 3

Range on `variable`: `price_error_bc` → `pv_error_bc`

| Column | Meaning |
|---|---|
| `variable` | project-specific; read by the scripts in `scripts/` |
| `mean_error` | project-specific; read by the scripts in `scripts/` |
| `std_error` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/reduction_diagnostics_50.csv`  (0.3 KiB)

Rows (excluding header): 5  |  Columns: 3

Range on `variable`: `price_error_bc` → `pv_error_bc`

| Column | Meaning |
|---|---|
| `variable` | project-specific; read by the scripts in `scripts/` |
| `mean_error` | project-specific; read by the scripts in `scripts/` |
| `std_error` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/scenario_reduced_100.csv`  (263.4 KiB)

Rows (excluding header): 2,400  |  Columns: 9

Range on `scenario_id`: `1` → `100`

| Column | Meaning |
|---|---|
| `scenario_id` | project-specific; read by the scripts in `scripts/` |
| `source_scenario_id` | project-specific; read by the scripts in `scripts/` |
| `hour` | project-specific; read by the scripts in `scripts/` |
| `probability` | project-specific; read by the scripts in `scripts/` |
| `price_error_bc` | project-specific; read by the scripts in `scripts/` |
| `load_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_on_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_off_error_bc` | project-specific; read by the scripts in `scripts/` |
| `pv_error_bc` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/scenario_reduced_30.csv`  (79.0 KiB)

Rows (excluding header): 720  |  Columns: 9

Range on `scenario_id`: `1` → `30`

| Column | Meaning |
|---|---|
| `scenario_id` | project-specific; read by the scripts in `scripts/` |
| `source_scenario_id` | project-specific; read by the scripts in `scripts/` |
| `hour` | project-specific; read by the scripts in `scripts/` |
| `probability` | project-specific; read by the scripts in `scripts/` |
| `price_error_bc` | project-specific; read by the scripts in `scripts/` |
| `load_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_on_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_off_error_bc` | project-specific; read by the scripts in `scripts/` |
| `pv_error_bc` | project-specific; read by the scripts in `scripts/` |

### `data/gate10/scenarios/reduced_scenarios/scenario_reduced_50.csv`  (131.9 KiB)

Rows (excluding header): 1,200  |  Columns: 9

Range on `scenario_id`: `1` → `50`

| Column | Meaning |
|---|---|
| `scenario_id` | project-specific; read by the scripts in `scripts/` |
| `source_scenario_id` | project-specific; read by the scripts in `scripts/` |
| `hour` | project-specific; read by the scripts in `scripts/` |
| `probability` | project-specific; read by the scripts in `scripts/` |
| `price_error_bc` | project-specific; read by the scripts in `scripts/` |
| `load_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_on_error_bc` | project-specific; read by the scripts in `scripts/` |
| `wind_off_error_bc` | project-specific; read by the scripts in `scripts/` |
| `pv_error_bc` | project-specific; read by the scripts in `scripts/` |

### `data/market/afrr_capacity_oos_2026_08.csv`  (25.8 KiB)

Rows (excluding header): 168  |  Columns: 24

Range on `DATE_FROM`: `2026-08-06` → `2026-08-19`

| Column | Meaning |
|---|---|
| `DATE_FROM` | project-specific; read by the scripts in `scripts/` |
| `DATE_TO` | project-specific; read by the scripts in `scripts/` |
| `TYPE_OF_RESERVES` | project-specific; read by the scripts in `scripts/` |
| `PRODUCT` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_SUM_OF_OFFERED_CAPACITY_[MW]` | project-specific; read by the scripts in `scripts/` |
| `requested_delivery_date` | project-specific; read by the scripts in `scripts/` |

### `data/market/afrr_capacity_summer_2026.csv`  (146.6 KiB)

Rows (excluding header): 984  |  Columns: 24

Range on `DATE_FROM`: `2026-06-01` → `2026-08-21`

| Column | Meaning |
|---|---|
| `DATE_FROM` | project-specific; read by the scripts in `scripts/` |
| `DATE_TO` | project-specific; read by the scripts in `scripts/` |
| `TYPE_OF_RESERVES` | project-specific; read by the scripts in `scripts/` |
| `PRODUCT` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `TOTAL_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `AUSTRIA_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_MIN_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_AVERAGE_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_MARGINAL_CAPACITY_PRICE_[(EUR/MW)/h]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_IMPORT(-)_EXPORT(+)_[MW]` | project-specific; read by the scripts in `scripts/` |
| `CZECH_REPUBLIC_ALLOCATED_VOLUME_[MW]` | project-specific; read by the scripts in `scripts/` |
| `GERMANY_SUM_OF_OFFERED_CAPACITY_[MW]` | project-specific; read by the scripts in `scripts/` |
| `requested_delivery_date` | project-specific; read by the scripts in `scripts/` |

### `data/market/manifest_oos_2026_08.json`  (12.8 KiB)

JSON object, 6 top-level keys: `period_local`, `retrieved_utc`, `market_panel`, `reserve_market_results`, `raw_source_sha256`, `limitations`

### `data/market/manifest_sept_2026.json`  (1.7 KiB)

JSON object, 7 top-level keys: `period_local`, `retrieved_utc`, `market_panel`, `fcr_capacity`, `mfrr_capacity`, `unavailable_inputs`, `notes`

### `data/market/manifest_summer_2026.json`  (61.5 KiB)

JSON object, 9 top-level keys: `period_local`, `retrieved_utc`, `market_panel`, `reserve_market_results`, `chunks`, `raw_source_sha256`, `normalized_output_sha256`, `additional_source_sha256`, `limitations`

### `data/market/market_panel_oos_2026_08_15min.csv`  (164.3 KiB)

Rows (excluding header): 1,344  |  Columns: 12

Range on `timestamp_utc`: `2026-08-05T22:00:00+00:00` → `2026-08-19T21:45:00+00:00`

| Column | Meaning |
|---|---|
| `timestamp_utc` | interval start, UTC |
| `timestamp_local` | interval start, Europe/Berlin local time |
| `day_local` | local calendar day |
| `interval_start_local` | local clock time of the interval start |
| `da_price_eur_mwh` | SMARD DE-LU day-ahead price, EUR/MWh |
| `rebap_eur_mwh` | German reBAP imbalance price, EUR/MWh (single price) |
| `rebap_undercovered_eur_mwh` | reBAP component for under-covered positions, EUR/MWh |
| `rebap_overcovered_eur_mwh` | reBAP component for over-covered positions, EUR/MWh |
| `load_actual_mw` | German actual load, MW |
| `solar_generation_mw` | German solar generation, MW |
| `wind_onshore_generation_mw` | German onshore wind generation, MW |
| `wind_offshore_generation_mw` | German offshore wind generation, MW |

### `data/market/market_panel_summer_2026_15min.csv`  (960.3 KiB)

Rows (excluding header): 7,872  |  Columns: 12

Range on `timestamp_utc`: `2026-05-31T22:00:00+00:00` → `2026-08-21T21:45:00+00:00`

| Column | Meaning |
|---|---|
| `timestamp_utc` | interval start, UTC |
| `timestamp_local` | interval start, Europe/Berlin local time |
| `day_local` | local calendar day |
| `interval_start_local` | local clock time of the interval start |
| `da_price_eur_mwh` | SMARD DE-LU day-ahead price, EUR/MWh |
| `rebap_eur_mwh` | German reBAP imbalance price, EUR/MWh (single price) |
| `rebap_undercovered_eur_mwh` | reBAP component for under-covered positions, EUR/MWh |
| `rebap_overcovered_eur_mwh` | reBAP component for over-covered positions, EUR/MWh |
| `load_actual_mw` | German actual load, MW |
| `solar_generation_mw` | German solar generation, MW |
| `wind_onshore_generation_mw` | German onshore wind generation, MW |
| `wind_offshore_generation_mw` | German offshore wind generation, MW |

### `data/study_b/smard_da_week.csv`  (21.2 KiB)

Rows (excluding header): 672  |  Columns: 2

Range on `timestamp`: `2026-04-05 22:00:00+00:00` → `2026-04-12 21:45:00+00:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `da_price` | project-specific; read by the scripts in `scripts/` |

### `data/study_b/smard_power_week.csv`  (35.9 KiB)

Rows (excluding header): 672  |  Columns: 5

Range on `timestamp`: `2026-04-05 22:00:00+00:00` → `2026-04-12 21:45:00+00:00`

| Column | Meaning |
|---|---|
| `timestamp` | interval timestamp |
| `Wind offshore` | project-specific; read by the scripts in `scripts/` |
| `Wind onshore` | project-specific; read by the scripts in `scripts/` |
| `Solar` | project-specific; read by the scripts in `scripts/` |
| `Load` | project-specific; read by the scripts in `scripts/` |

## `results/`

### `results/gate10/Gate10_RUN_REPORT.json`  (4.7 KiB)

JSON object, 7 top-level keys: `gate`, `timestamp`, `optimization_results`, `scenario_diagnostics`, `B0_reference_profit`, `config_file`, `config_status`

### `results/gate10/Optimization_Summary.csv`  (1.1 KiB)

Rows (excluding header): 7  |  Columns: 10

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `K` | number of joint scenarios |
| `expected_profit` | project-specific; read by the scripts in `scripts/` |
| `cvar95` | project-specific; read by the scripts in `scripts/` |
| `risk_adjusted_objective` | project-specific; read by the scripts in `scripts/` |
| `worst_case_profit` | project-specific; read by the scripts in `scripts/` |
| `best_case_profit` | project-specific; read by the scripts in `scripts/` |
| `runtime_seconds` | project-specific; read by the scripts in `scripts/` |
| `status` | project-specific; read by the scripts in `scripts/` |
| `variables` | project-specific; read by the scripts in `scripts/` |

### `results/gate10/Realized_Settlement_Summary.csv`  (0.5 KiB)

Rows (excluding header): 7  |  Columns: 6

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `K` | number of joint scenarios |
| `lambda` | project-specific; read by the scripts in `scripts/` |
| `realized_settlement_profit_eur` | project-specific; read by the scripts in `scripts/` |
| `mean_abs_imbalance_mw` | project-specific; read by the scripts in `scripts/` |
| `total_unserved_mwh` | project-specific; read by the scripts in `scripts/` |

### `results/gate10/p1_riskneutral_K100.csv`  (0.2 KiB)

Rows (excluding header): 1  |  Columns: 10

Range on `model`: `P1` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `lambda_risk` | project-specific; read by the scripts in `scripts/` |
| `reserve_price` | project-specific; read by the scripts in `scripts/` |
| `K` | number of joint scenarios |
| `expected_profit` | project-specific; read by the scripts in `scripts/` |
| `cvar95` | project-specific; read by the scripts in `scripts/` |
| `risk_adjusted` | project-specific; read by the scripts in `scripts/` |
| `worst_case` | project-specific; read by the scripts in `scripts/` |
| `best_case` | project-specific; read by the scripts in `scripts/` |
| `runtime_s` | project-specific; read by the scripts in `scripts/` |

### `results/gate10/rebap_summary.csv`  (0.5 KiB)

Rows (excluding header): 1  |  Columns: 18

Range on `panel`: `summer 2026 (1 Jun-21 Aug)` → `summer 2026 (1 Jun-21 Aug)`

| Column | Meaning |
|---|---|
| `panel` | project-specific; read by the scripts in `scripts/` |
| `n_hourly` | project-specific; read by the scripts in `scripts/` |
| `n_days` | number of evaluated days |
| `da_mean` | project-specific; read by the scripts in `scripts/` |
| `da_median` | project-specific; read by the scripts in `scripts/` |
| `da_min` | project-specific; read by the scripts in `scripts/` |
| `da_max` | project-specific; read by the scripts in `scripts/` |
| `da_std` | project-specific; read by the scripts in `scripts/` |
| `rebap_mean` | project-specific; read by the scripts in `scripts/` |
| `rebap_median` | project-specific; read by the scripts in `scripts/` |
| `rebap_min` | project-specific; read by the scripts in `scripts/` |
| `rebap_max` | project-specific; read by the scripts in `scripts/` |
| `rebap_std` | project-specific; read by the scripts in `scripts/` |
| `rebap_minus_da_mean` | project-specific; read by the scripts in `scripts/` |
| `rebap_minus_da_median` | project-specific; read by the scripts in `scripts/` |
| `corr_da_rebap` | project-specific; read by the scripts in `scripts/` |
| `share_hours_rebap_gt_da` | project-specific; read by the scripts in `scripts/` |
| `single_price` | project-specific; read by the scripts in `scripts/` |

### `results/gate10/sweep_reserve_price_K100.csv`  (2.5 KiB)

Rows (excluding header): 14  |  Columns: 14

Range on `reserve_price_eur_per_mw`: `0.0` → `7.5`

| Column | Meaning |
|---|---|
| `reserve_price_eur_per_mw` | project-specific; read by the scripts in `scripts/` |
| `pct_of_proxy` | project-specific; read by the scripts in `scripts/` |
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `lambda_risk` | project-specific; read by the scripts in `scripts/` |
| `K` | number of joint scenarios |
| `expected_profit` | project-specific; read by the scripts in `scripts/` |
| `cvar95` | project-specific; read by the scripts in `scripts/` |
| `risk_adjusted` | project-specific; read by the scripts in `scripts/` |
| `worst_case` | project-specific; read by the scripts in `scripts/` |
| `best_case` | project-specific; read by the scripts in `scripts/` |
| `runtime_s` | project-specific; read by the scripts in `scripts/` |
| `status` | project-specific; read by the scripts in `scripts/` |
| `mean_RES_mw` | project-specific; read by the scripts in `scripts/` |
| `reserve_revenue_eur` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ac_check.csv`  (0.3 KiB)

Rows (excluding header): 2  |  Columns: 6

Range on `model`: `B2` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `mean_abs_err_pu` | project-specific; read by the scripts in `scripts/` |
| `max_abs_err_pu` | project-specific; read by the scripts in `scripts/` |
| `p95_abs_err_pu` | project-specific; read by the scripts in `scripts/` |
| `ld_vmin` | LinDistFlow minimum voltage, pu |
| `ac_vmin` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ac_triple.csv`  (0.6 KiB)

Rows (excluding header): 3  |  Columns: 10

Range on `model`: `B2` → `P0`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `ld_vmin` | LinDistFlow minimum voltage, pu |
| `bfs_vmin` | project-specific; read by the scripts in `scripts/` |
| `nr_vmin` | Newton-Raphson minimum voltage, pu |
| `bfs_mean` | project-specific; read by the scripts in `scripts/` |
| `bfs_max` | project-specific; read by the scripts in `scripts/` |
| `nr_mean` | project-specific; read by the scripts in `scripts/` |
| `nr_max` | project-specific; read by the scripts in `scripts/` |
| `nr_p95` | project-specific; read by the scripts in `scripts/` |
| `nr_conv_hours` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/case_results.csv`  (0.5 KiB)

Rows (excluding header): 3  |  Columns: 13

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `throughput` | project-specific; read by the scripts in `scripts/` |
| `day` | day identifier used by the Study-B runner |

### `results/study_b/epsilon_v.json`  (0.2 KiB)

JSON object, 4 top-level keys: `nr_p1_max_dV`, `nr_p1_mean_dV`, `epsilon_v_suggested`, `note`

### `results/study_b/fdia_residual.json`  (0.4 KiB)

JSON object, 15 top-level keys: `detector`, `sigma_pu`, `bias_pu`, `theta_99`, `n_mc`, `tp`, `fp`, `fn`, `tn`, `precision`, `recall`, `clean_profit`, `attack_bid_profit`, `attack_bid_dprofit`, `attack_bid_ok`

### `results/study_b/fdia_suite.json`  (2.1 KiB)

JSON object, 6 top-level keys: `theta_residual`, `theta_zscore`, `sigma`, `n_mc`, `attacks`, `economic`

### `results/study_b/pq_ablation.csv`  (0.9 KiB)

Rows (excluding header): 8  |  Columns: 11

Range on `vmin_set`: `0.93` → `0.95`

| Column | Meaning |
|---|---|
| `vmin_set` | project-specific; read by the scripts in `scripts/` |
| `strategy` | project-specific; read by the scripts in `scripts/` |
| `ok` | project-specific; read by the scripts in `scripts/` |
| `profit` | realized settlement profit, EUR/day |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `q_abs` | project-specific; read by the scripts in `scripts/` |
| `thr` | throughput term charged in the objective, EUR/day |
| `imb` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/rainflow.csv`  (0.9 KiB)

Rows (excluding header): 6  |  Columns: 8

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `throughput_mwh` | project-specific; read by the scripts in `scripts/` |
| `efc_throughput` | project-specific; read by the scripts in `scripts/` |
| `efc_rainflow` | project-specific; read by the scripts in `scripts/` |
| `xu_eur` | project-specific; read by the scripts in `scripts/` |
| `aging_thr_eur` | project-specific; read by the scripts in `scripts/` |
| `soc_min` | project-specific; read by the scripts in `scripts/` |
| `soc_max` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ramp.csv`  (0.4 KiB)

Rows (excluding header): 4  |  Columns: 8

Range on `ramp`: `0.0` → `0.05`

| Column | Meaning |
|---|---|
| `ramp` | project-specific; read by the scripts in `scripts/` |
| `ok` | project-specific; read by the scripts in `scripts/` |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `thr` | throughput term charged in the objective, EUR/day |
| `time_s` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/seed_results.csv`  (10.3 KiB)

Rows (excluding header): 30  |  Columns: 31

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `day` | day identifier used by the Study-B runner |
| `seed` | random seed of the scenario draw |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `da_status` | project-specific; read by the scripts in `scripts/` |
| `rt_status` | project-specific; read by the scripts in `scripts/` |
| `da_gap` | project-specific; read by the scripts in `scripts/` |
| `rt_gap` | project-specific; read by the scripts in `scripts/` |
| `da_time_s` | project-specific; read by the scripts in `scripts/` |
| `rt_time_s` | project-specific; read by the scripts in `scripts/` |
| `time_s` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `v_rms_und` | project-specific; read by the scripts in `scripts/` |
| `v_max_und` | project-specific; read by the scripts in `scripts/` |
| `n_hour_viol` | project-specific; read by the scripts in `scripts/` |
| `n_episode` | project-specific; read by the scripts in `scripts/` |
| `max_episode_h` | project-specific; read by the scripts in `scripts/` |
| `mean_episode_h` | project-specific; read by the scripts in `scripts/` |
| `s_max_mva` | project-specific; read by the scripts in `scripts/` |
| `n_line_viol` | project-specific; read by the scripts in `scripts/` |
| `q_abs_mvarh` | project-specific; read by the scripts in `scripts/` |
| `throughput` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/sensitivity.csv`  (6.3 KiB)

Rows (excluding header): 18  |  Columns: 33

Range on `model`: `B2` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `day` | day identifier used by the Study-B runner |
| `seed` | random seed of the scenario draw |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `da_status` | project-specific; read by the scripts in `scripts/` |
| `rt_status` | project-specific; read by the scripts in `scripts/` |
| `da_gap` | project-specific; read by the scripts in `scripts/` |
| `rt_gap` | project-specific; read by the scripts in `scripts/` |
| `da_time_s` | project-specific; read by the scripts in `scripts/` |
| `rt_time_s` | project-specific; read by the scripts in `scripts/` |
| `time_s` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `v_rms_und` | project-specific; read by the scripts in `scripts/` |
| `v_max_und` | project-specific; read by the scripts in `scripts/` |
| `n_hour_viol` | project-specific; read by the scripts in `scripts/` |
| `n_episode` | project-specific; read by the scripts in `scripts/` |
| `max_episode_h` | project-specific; read by the scripts in `scripts/` |
| `mean_episode_h` | project-specific; read by the scripts in `scripts/` |
| `s_max_mva` | project-specific; read by the scripts in `scripts/` |
| `n_line_viol` | project-specific; read by the scripts in `scripts/` |
| `q_abs_mvarh` | project-specific; read by the scripts in `scripts/` |
| `throughput` | project-specific; read by the scripts in `scripts/` |
| `sweep` | project-specific; read by the scripts in `scripts/` |
| `param` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/table_iii_means.csv`  (0.4 KiB)

Rows (excluding header): 4  |  Columns: 7

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `profit` | realized settlement profit, EUR/day |
| `worst` | project-specific; read by the scripts in `scripts/` |
| `viol` | count of voltage violations in that run |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `n` | project-specific; read by the scripts in `scripts/` |
| `all_kOptimal` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/v95_try.csv`  (1.5 KiB)

Rows (excluding header): 4  |  Columns: 33

Range on `model`: `P1` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `day` | day identifier used by the Study-B runner |
| `seed` | random seed of the scenario draw |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `da_status` | project-specific; read by the scripts in `scripts/` |
| `rt_status` | project-specific; read by the scripts in `scripts/` |
| `da_gap` | project-specific; read by the scripts in `scripts/` |
| `rt_gap` | project-specific; read by the scripts in `scripts/` |
| `da_time_s` | project-specific; read by the scripts in `scripts/` |
| `rt_time_s` | project-specific; read by the scripts in `scripts/` |
| `time_s` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `v_rms_und` | project-specific; read by the scripts in `scripts/` |
| `v_max_und` | project-specific; read by the scripts in `scripts/` |
| `n_hour_viol` | project-specific; read by the scripts in `scripts/` |
| `n_episode` | project-specific; read by the scripts in `scripts/` |
| `max_episode_h` | project-specific; read by the scripts in `scripts/` |
| `mean_episode_h` | project-specific; read by the scripts in `scripts/` |
| `s_max_mva` | project-specific; read by the scripts in `scripts/` |
| `n_line_viol` | project-specific; read by the scripts in `scripts/` |
| `q_abs_mvarh` | project-specific; read by the scripts in `scripts/` |
| `throughput` | project-specific; read by the scripts in `scripts/` |
| `inv_head` | project-specific; read by the scripts in `scripts/` |
| `v_min_set` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/week_results.csv`  (14.2 KiB)

Rows (excluding header): 42  |  Columns: 31

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `day` | day identifier used by the Study-B runner |
| `seed` | random seed of the scenario draw |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `da_status` | project-specific; read by the scripts in `scripts/` |
| `rt_status` | project-specific; read by the scripts in `scripts/` |
| `da_gap` | project-specific; read by the scripts in `scripts/` |
| `rt_gap` | project-specific; read by the scripts in `scripts/` |
| `da_time_s` | project-specific; read by the scripts in `scripts/` |
| `rt_time_s` | project-specific; read by the scripts in `scripts/` |
| `time_s` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `v_rms_und` | project-specific; read by the scripts in `scripts/` |
| `v_max_und` | project-specific; read by the scripts in `scripts/` |
| `n_hour_viol` | project-specific; read by the scripts in `scripts/` |
| `n_episode` | project-specific; read by the scripts in `scripts/` |
| `max_episode_h` | project-specific; read by the scripts in `scripts/` |
| `mean_episode_h` | project-specific; read by the scripts in `scripts/` |
| `s_max_mva` | project-specific; read by the scripts in `scripts/` |
| `n_line_viol` | project-specific; read by the scripts in `scripts/` |
| `q_abs_mvarh` | project-specific; read by the scripts in `scripts/` |
| `throughput` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/wilcoxon.json`  (0.8 KiB)

JSON object, 4 top-level keys: `profit`, `n_viol`, `vmin`, `aging`

### `results/study_b/ext/e1_nr_multiday.csv`  (1.7 KiB)

Rows (excluding header): 14  |  Columns: 10

Range on `day`: `2026-04-06` → `2026-04-12`

| Column | Meaning |
|---|---|
| `day` | day identifier used by the Study-B runner |
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `ld_vmin` | LinDistFlow minimum voltage, pu |
| `nr_vmin` | Newton-Raphson minimum voltage, pu |
| `nr_nviol` | NR bus-hours below the voltage floor |
| `nr_hours` | NR solves performed |
| `nr_mean_err` | mean |V_NR - V_LD|, pu |
| `nr_max_err` | max |V_NR - V_LD|, pu |
| `nr_p95_err` | project-specific; read by the scripts in `scripts/` |
| `ld_noV` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e2_cdeg_sweep.csv`  (2.0 KiB)

Rows (excluding header): 30  |  Columns: 6

Range on `cdeg`: `3.0` → `20.0`

| Column | Meaning |
|---|---|
| `cdeg` | project-specific; read by the scripts in `scripts/` |
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `profit_mean` | project-specific; read by the scripts in `scripts/` |
| `viol_mean` | project-specific; read by the scripts in `scripts/` |
| `thr_mean` | project-specific; read by the scripts in `scripts/` |
| `aging_mean` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e3_alpha_K.csv`  (0.8 KiB)

Rows (excluding header): 12  |  Columns: 6

Range on `alpha`: `0.8` → `0.95`

| Column | Meaning |
|---|---|
| `alpha` | project-specific; read by the scripts in `scripts/` |
| `K` | number of joint scenarios |
| `expected_tail` | project-specific; read by the scripts in `scripts/` |
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `profit_mean` | project-specific; read by the scripts in `scripts/` |
| `viol_mean` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e4_polygon.csv`  (1.2 KiB)

Rows (excluding header): 14  |  Columns: 7

Range on `day`: `2026-04-06` → `2026-04-12`

| Column | Meaning |
|---|---|
| `day` | day identifier used by the Study-B runner |
| `variant` | project-specific; read by the scripts in `scripts/` |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `viol` | count of voltage violations in that run |
| `thr` | throughput term charged in the objective, EUR/day |
| `q_abs` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e5_f11_diag.csv`  (1.3 KiB)

Rows (excluding header): 21  |  Columns: 7

Range on `day`: `2026-04-06` → `2026-04-12`

| Column | Meaning |
|---|---|
| `day` | day identifier used by the Study-B runner |
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `profit` | realized settlement profit, EUR/day |
| `viol` | count of voltage violations in that run |
| `thr` | throughput term charged in the objective, EUR/day |
| `n_episodes` | project-specific; read by the scripts in `scripts/` |
| `max_ep` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e6a_radius_sweep.csv`  (0.3 KiB)

Rows (excluding header): 6  |  Columns: 8

Range on `delta_pu`: `0.002` → `0.012`

| Column | Meaning |
|---|---|
| `delta_pu` | project-specific; read by the scripts in `scripts/` |
| `tp` | project-specific; read by the scripts in `scripts/` |
| `fp` | project-specific; read by the scripts in `scripts/` |
| `fn` | project-specific; read by the scripts in `scripts/` |
| `tn` | project-specific; read by the scripts in `scripts/` |
| `recall` | project-specific; read by the scripts in `scripts/` |
| `precision` | project-specific; read by the scripts in `scripts/` |
| `fpr` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/ext/e6b_nr_mismatch.csv`  (0.2 KiB)

Rows (excluding header): 3  |  Columns: 8

Range on `delta_pu`: `0.004` → `0.012`

| Column | Meaning |
|---|---|
| `delta_pu` | project-specific; read by the scripts in `scripts/` |
| `tp` | project-specific; read by the scripts in `scripts/` |
| `fp` | project-specific; read by the scripts in `scripts/` |
| `fn` | project-specific; read by the scripts in `scripts/` |
| `tn` | project-specific; read by the scripts in `scripts/` |
| `recall` | project-specific; read by the scripts in `scripts/` |
| `precision` | project-specific; read by the scripts in `scripts/` |
| `fpr` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/solutions/B0_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B0_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B1a_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B1a_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B1b_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B1b_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B2_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/B2_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/P0_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/P0_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/P1_2026-04-06.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/P1_2026-04-08.npz`  (23.3 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/PQ_P-Q_2026-04-08.npz`  (6.9 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/PQ_P-Q_no_V_2026-04-08.npz`  (6.9 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/PQ_P-only_2026-04-08.npz`  (6.9 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/solutions/PQ_Q-only_2026-04-08.npz`  (6.9 KiB)

NumPy `.npz` archive; keys documented in `results/study_b/solutions/README.md`.

### `results/study_b/v937/b3_rebap_gap_daily.csv`  (1.1 KiB)

Rows (excluding header): 14  |  Columns: 8

Range on `day`: `2026-08-06` → `2026-08-19`

| Column | Meaning |
|---|---|
| `day` | day identifier used by the Study-B runner |
| `da_mean` | project-specific; read by the scripts in `scripts/` |
| `rebap_mean` | project-specific; read by the scripts in `scripts/` |
| `lminus_mean` | project-specific; read by the scripts in `scripts/` |
| `lplus_mean` | project-specific; read by the scripts in `scripts/` |
| `gap_minus_mean` | project-specific; read by the scripts in `scripts/` |
| `gap_plus_mean` | project-specific; read by the scripts in `scripts/` |
| `gap_minus_eur_per_mwh` | project-specific; read by the scripts in `scripts/` |

### `results/study_b/v937/studyb_overlap_archived_days.csv`  (1.1 KiB)

Rows (excluding header): 12  |  Columns: 7

Range on `file`: `B0_2026-04-06.npz` → `P1_2026-04-08.npz`

| Column | Meaning |
|---|---|
| `file` | archived .npz solution file |
| `shape` | project-specific; read by the scripts in `scripts/` |
| `total_overlap_mwh` | sum of min(p_charge, p_discharge), MWh/day |
| `max_hour_overlap_mw` | project-specific; read by the scripts in `scripts/` |
| `overlap_hours` | project-specific; read by the scripts in `scripts/` |
| `total_ch` | total charging energy, MWh/day |
| `total_dis` | total discharging energy, MWh/day |

### `results/study_b/v937/week_v937.csv`  (14.3 KiB)

Rows (excluding header): 42  |  Columns: 31

Range on `model`: `B0` → `P1`

| Column | Meaning |
|---|---|
| `model` | model label (B0, B1a, B1b, B2, P0, P1, or a P/Q ablation variant) |
| `day` | day identifier used by the Study-B runner |
| `seed` | random seed of the scenario draw |
| `da_ok` | project-specific; read by the scripts in `scripts/` |
| `rt_ok` | project-specific; read by the scripts in `scripts/` |
| `da_status` | project-specific; read by the scripts in `scripts/` |
| `rt_status` | project-specific; read by the scripts in `scripts/` |
| `da_gap` | project-specific; read by the scripts in `scripts/` |
| `rt_gap` | project-specific; read by the scripts in `scripts/` |
| `da_time_s` | project-specific; read by the scripts in `scripts/` |
| `rt_time_s` | project-specific; read by the scripts in `scripts/` |
| `time_s` | project-specific; read by the scripts in `scripts/` |
| `pda_mwh` | project-specific; read by the scripts in `scripts/` |
| `da_rev` | project-specific; read by the scripts in `scripts/` |
| `imb` | project-specific; read by the scripts in `scripts/` |
| `aging` | aging/degradation cost charged in the objective, EUR/day |
| `profit` | realized settlement profit, EUR/day |
| `vmin` | minimum bus voltage magnitude, pu |
| `vmax` | project-specific; read by the scripts in `scripts/` |
| `n_viol` | count of bus-hour voltage-limit violations (LinDistFlow) |
| `n_viol_095` | project-specific; read by the scripts in `scripts/` |
| `v_rms_und` | project-specific; read by the scripts in `scripts/` |
| `v_max_und` | project-specific; read by the scripts in `scripts/` |
| `n_hour_viol` | project-specific; read by the scripts in `scripts/` |
| `n_episode` | project-specific; read by the scripts in `scripts/` |
| `max_episode_h` | project-specific; read by the scripts in `scripts/` |
| `mean_episode_h` | project-specific; read by the scripts in `scripts/` |
| `s_max_mva` | project-specific; read by the scripts in `scripts/` |
| `n_line_viol` | project-specific; read by the scripts in `scripts/` |
| `q_abs_mvarh` | project-specific; read by the scripts in `scripts/` |
| `throughput` | project-specific; read by the scripts in `scripts/` |
