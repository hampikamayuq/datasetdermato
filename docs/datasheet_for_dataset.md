# Datasheet for Dataset

This template follows the spirit of Datasheets for Datasets and should be completed for every dataset release.

## Motivation

- What is the purpose of the dataset?
- Which dermatology services or research questions motivated it?
- Who created the dataset?
- Who funded or supported the dataset?

## Composition

- Number of patients:
- Number of cases:
- Number of lesions:
- Number of images:
- Image modalities:
  - clinical
  - dermoscopy
  - surgical
  - histopathology
- Date or acquisition period:
- Source types represented:
- Specialty services represented:
- Diagnostic groups represented:
- Evidence levels represented:
  - bronze
  - silver
  - gold

## Patient and Case Metadata

Document availability and missingness for:

- age or age group
- sex
- Fitzpatrick skin type or equivalent skin tone measure
- geographic region
- care setting
- body site
- symptoms
- evolution time
- previous treatment
- recurrence
- immunosuppression

## Collection Process

- How were cases identified?
- Were cases identified from pathology archives, clinical archives, faculty collections, resident collections, research projects, or institutional databases?
- Were images linked to pathology reports or follow-up?
- Were inclusion and exclusion criteria predefined?
- How were duplicates handled?

## Annotation and Review

- Who annotated diagnoses?
- How many expert reviewers were involved?
- Was there consensus review?
- Was histopathology available?
- How were disagreements resolved?
- Are masks, bounding boxes, or polygons available?

## Preprocessing and Anonymization

- Was EXIF metadata removed?
- Were patient identifiers removed?
- Were faces, tattoos, labels, dates, or record numbers reviewed?
- Were images cropped, blurred, resized, or color-normalized?
- Are original images retained in restricted storage?

## Splits

- Are train/validation/test splits predefined?
- Are splits patient-level?
- Are lesion-level or case-level splits needed?
- Has leakage across splits been audited?

## Distribution and Access

- Access class:
  - internal research
  - controlled access
  - public metadata only
  - public release
- License:
- Data Use Agreement:
- Redistribution policy:
- Reidentification policy:

## Ethics and Legal

- CEP/CONEP approval:
- Consent status:
- Consent waiver:
- LGPD risk assessment:
- Data controller or steward:

## Uses

Recommended uses:

- dataset curation research
- model development
- external validation
- fairness analysis
- education, when allowed

Out-of-scope uses:

- clinical diagnosis without validation
- commercial medical device use without regulatory review
- reidentification attempts
- unrestricted redistribution of controlled data

## Maintenance

- Dataset version:
- Release date:
- Maintainer:
- Update process:
- Takedown or correction process:
- Known limitations:
