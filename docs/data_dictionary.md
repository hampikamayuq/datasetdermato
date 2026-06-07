# Data Dictionary

This dictionary summarizes project-specific fields for `dermatology-service-dataset`.

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
- `source_type`: origin of the case or image archive.
- `specialty_service`: dermatology subspecialty or service line.
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

Allowed `source_type` values:

- `faculty_collection`
- `resident_collection`
- `pathology_archive`
- `clinical_archive`
- `conference_archive`
- `research_project`
- `private_practice_archive`
- `institutional_database`

Allowed `specialty_service` values:

- `general_dermatology`
- `pediatric_dermatology`
- `dermatologic_surgery`
- `dermatopathology`
- `oncologic_dermatology`
- `trichology`
- `hanseniasis`
- `autoimmune_skin_disease`
- `contact_dermatitis`
- `pigmented_lesions`
- `inflammatory_skin_disease`
- `infectious_dermatology`
- `tropical_dermatology`
- `cutaneous_tumors`
- `dermoscopy`

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

## surgical_procedures

- `procedure_id`: internal UUID
- `case_id`: case foreign key
- `procedure_type`: biopsy, excision, Mohs surgery, curettage, etc.
- `procedure_date`: procedure date, when ethically allowed
- `body_site`: surgical site
- `surgical_margins_planned`: planned margins
- `specimen_id_hash`: hashed specimen identifier
- `surgeon_id_hash`: hashed surgeon identifier

## expert_reviews

- `reviewer_id_hash`: hashed reviewer identifier
- `reviewer_specialty`: dermatologist, dermatopathologist, surgeon, resident, etc.
- `diagnosis`: reviewer diagnosis
- `consensus_diagnosis`: consensus diagnosis, when available
- `confidence_score`: 1 to 5
- `image_quality`: 1 to 5
- `agreement_level`: single expert, double agreement, consensus, etc.
- `review_status`: review workflow state

## clinical_followups

- `followup_id`: internal UUID
- `case_id`: case foreign key
- `followup_date`: follow-up date, when ethically allowed
- `recurrence`: recurrence present
- `progression`: disease progression present
- `metastasis`: metastasis present
- `treatment_response`: response description
- `outcome_status`: active disease, no evidence of disease, lost to follow-up, death, etc.
