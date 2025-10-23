# Changelog

All notable changes to the Student Performance Prediction backend will be documented in this file.

## [1.1.1] - 2025-10-23
- Fixed constant prediction issue by validating feature mapping and ensuring `previous_grade` is consistently used in training and inference.
- Added `GET /dataset-stats` endpoint to expose dataset distribution statistics for diagnostics.
- Hardened categorical normalization across code paths to avoid unseen-category collapse.

## [1.1.0] - 2025-10-23
- Added explicit backend version `API_VERSION` exposed via `GET /`.
- Included `previous_grade` as a numeric feature in model training and preprocessing, improving prediction quality and variability.
- Refactored dataset mapping into helper functions (`_map_df1`, `_map_df2`, `_map_df3`) for consistency across training and batch prediction.
- Introduced `GET /batch-predict` endpoint to generate predictions for full datasets and attach a new `PredictedGrade` column while preserving all original attributes.
- Batch prediction can optionally save enriched CSVs under `data/`.
- Minor cleanup to ensure consistent categorical normalization across code paths.

## [1.0.0] - 2025-10-20
- Initial FastAPI implementation with `GET /`, `GET /model-info`, and `POST /predict` endpoints.
- Combined training over three datasets with imputation and preprocessing.