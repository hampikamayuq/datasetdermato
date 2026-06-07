# Publication Guidelines

Use this document to choose reporting standards for studies based on the dataset.

## Dataset Release Paper

Use:

- Datasheets for Datasets
- Dataset card
- Quality audit report
- Ethics and access documentation

Report:

- number of patients, cases, lesions, and images
- acquisition period
- modalities
- source types
- specialty services
- diagnostic groups
- evidence levels
- skin tone distribution
- train/validation/test policy
- duplicate and leakage audit
- licensing and access restrictions

## Prediction Model Development or Validation

Use TRIPOD+AI when the study develops or validates a prediction model using regression or machine learning.

Report:

- target population
- prediction task
- inclusion and exclusion criteria
- predictors and outcome definition
- reference standard
- missing data handling
- model development and validation design
- calibration and discrimination
- subgroup analysis

## Diagnostic Accuracy Study

Use STARD-AI when the study evaluates diagnostic accuracy of an AI system.

Report:

- index test
- reference standard
- diagnostic threshold
- test set construction
- patient flow
- uncertainty intervals
- subgroup performance
- failure modes

## Clinical Trial

Use CONSORT-AI when an AI intervention is tested in a clinical trial.

Report:

- intervention workflow
- user interaction with AI
- human oversight
- failure handling
- protocol deviations
- clinical outcomes
- safety endpoints

## Not Yet Covered

This repository organizes data and metadata. It does not itself validate a model for clinical use.
