# Data Dictionary

This dictionary summarizes project-specific fields beyond the ISIC reference files in `references/`.

## patients

- `patient_id`: internal UUID
- `patient_hash`: salted hash of institutional identifier
- `sex`: sex recorded in clinical metadata
- `birth_year`: year of birth, when allowed
- `age_at_case`: approximate age at case date
- `age_group`: grouped age range
- `fitzpatrick_type`: Fitzpatrick skin type, 1 to 6
- `geographic_region`: broad region only
- `care_setting`: public, private, university, or other

## cases

- `case_id`: internal UUID
- `patient_id`: patient foreign key
- `specialty`: dermatopediatrics, dermatologic surgery, dermatopathology, oncology, etc.
- `body_site`: anatomic site
- `evolution_time`: time since lesion or disease onset
- `symptoms`: pain, pruritus, bleeding, asymptomatic, etc.
- `previous_treatment`: treatment before image acquisition
- `recurrence`: whether case represents recurrence
- `immunosuppression`: whether immunosuppression is present
- `diagnosis_primary`: most specific diagnosis
- `diagnosis_secondary`: secondary diagnosis or differential
- `diagnosis_group`: broad disease group
- `cid10`: ICD-10 code
- `cid11`: ICD-11 code
- `snomed_ct`: SNOMED CT code, when available
- `certainty_grade`: diagnostic certainty
- `confirmation_method`: clinical, dermoscopy, histopathology, follow-up, consensus
- `evidence_level`: bronze, silver, or gold

## images

- `image_type`: clinical, dermoscopy, pathology, surgical, histopathology
- `device`: camera or acquisition device
- `width`: image width in pixels
- `height`: image height in pixels
- `illumination`: natural light, flash, polarized, unknown, etc.
- `approximate_distance`: distance estimate, when known
- `has_scale`: whether image contains a ruler or scale
- `quality_score`: low, medium, high, or numeric score
- `anonymization_status`: pending, exif_removed, reviewed, rejected
- `has_identifying_risk`: whether image may identify a patient

## pathology_reports

- `histological_diagnosis`: diagnosis from pathology report
- `histological_type`: histologic type
- `subtype`: subtype
- `margins`: margin status
- `breslow_mm`: Breslow thickness in mm
- `clark_level`: Clark level
- `ulceration`: ulceration present
- `mitotic_index`: mitotic index
- `perineural_invasion`: perineural invasion present
- `immunohistochemistry`: relevant immunohistochemistry markers

## expert_reviews

- `reviewer_id_hash`: hashed reviewer identifier
- `reviewer_specialty`: dermatologist, dermatopathologist, surgeon, resident, etc.
- `diagnosis`: reviewer diagnosis
- `consensus_diagnosis`: consensus diagnosis, when available
- `confidence_score`: 1 to 5
- `image_quality`: 1 to 5
- `agreement_level`: single expert, double agreement, consensus, etc.
- `review_status`: review workflow state
