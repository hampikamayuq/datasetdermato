# Dataset Card

## Dataset name

datasetdermato

## Intended use

Research and development of dermatology image organization, labeling, preprocessing, and model prototyping workflows.

## Out-of-scope use

- Clinical diagnosis without medical validation
- Commercial medical device use without regulatory review
- Redistribution of restricted third-party images

## Data sources

Initial source candidates:

- DermNetNZ dermatology atlas pages
- ISIC Archive metadata conventions as external inspiration
- Public dataset candidates listed in the Skinive review

## Data fields

Primary metadata fields follow the project core metadata template, inspired by dermatology dataset conventions:

- image type
- dermoscopic type
- age
- sex
- anatomic site
- Fitzpatrick skin type
- lesion and patient identifiers
- diagnosis
- diagnosis confirmation type

## Known risks

- Label noise from educational pages or non-expert extraction
- Class imbalance
- Skin tone and geography bias
- Licensing constraints
- Patient re-identification risk in clinical photos

## Recommended evaluation

Track metrics by:

- diagnosis
- image type
- skin tone, when ethically available
- anatomic site
- source
- train/validation/test split
