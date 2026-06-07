# Fairness and Bias Plan

Dermatology AI datasets should be evaluated for representativeness and subgroup robustness.

## Required Subgroup Fields

When ethically available, track:

- Fitzpatrick skin type or equivalent skin tone measure
- age group
- sex
- geographic region
- body site
- care setting
- source type
- specialty service
- image modality
- diagnosis group

## Descriptive Statistics

For every dataset version, report:

- image count by subgroup
- patient count by subgroup
- case count by subgroup
- diagnosis distribution by subgroup
- evidence level by subgroup
- missingness by subgroup

## Model Evaluation

For model studies, report performance by:

- skin tone
- diagnosis group
- benign/malignant category
- image modality
- source type
- specialty service
- care setting
- age group
- sex

Recommended metrics:

- sensitivity
- specificity
- balanced accuracy
- AUROC/AUPRC when appropriate
- calibration
- false negative rate
- false positive rate

## Bias Risks

Known risks:

- overrepresentation of lighter skin tones
- underrepresentation of rare diseases
- source-specific artifacts
- referral-center bias
- surgical/pathology enrichment bias
- duplicated educational images
- inconsistent labels across services

## Mitigation

Recommended mitigations:

- patient-level splits
- external validation by source or institution
- source-type-stratified evaluation
- specialty-service-stratified evaluation
- minimum subgroup count reporting
- explicit uncertainty for underrepresented groups
