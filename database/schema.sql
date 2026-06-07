CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE patients (
  patient_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_hash TEXT UNIQUE NOT NULL,
  sex TEXT,
  birth_year INTEGER,
  age_at_case INTEGER,
  age_group TEXT,
  fitzpatrick_type INTEGER,
  geographic_region TEXT,
  care_setting TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE cases (
  case_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(patient_id),
  source_type TEXT CHECK (source_type IN (
    'faculty_collection',
    'resident_collection',
    'pathology_archive',
    'clinical_archive',
    'conference_archive',
    'research_project',
    'private_practice_archive',
    'institutional_database'
  )),
  specialty_service TEXT CHECK (specialty_service IN (
    'general_dermatology',
    'pediatric_dermatology',
    'dermatologic_surgery',
    'dermatopathology',
    'oncologic_dermatology',
    'trichology',
    'hanseniasis',
    'autoimmune_skin_disease',
    'contact_dermatitis',
    'pigmented_lesions',
    'inflammatory_skin_disease',
    'infectious_dermatology',
    'tropical_dermatology',
    'cutaneous_tumors',
    'dermoscopy'
  )),
  body_site TEXT,
  evolution_time TEXT,
  symptoms TEXT,
  previous_treatment TEXT,
  recurrence BOOLEAN,
  immunosuppression BOOLEAN,
  clinical_diagnosis TEXT,
  final_diagnosis TEXT,
  diagnosis_primary TEXT,
  diagnosis_secondary TEXT,
  diagnosis_group TEXT,
  cid10 TEXT,
  cid11 TEXT,
  snomed_ct TEXT,
  certainty_grade TEXT,
  confirmation_method TEXT,
  evidence_level TEXT CHECK (evidence_level IN ('bronze', 'silver', 'gold')),
  diagnosis_source TEXT,
  case_date DATE,
  dataset_version TEXT,
  source_site TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE images (
  image_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID NOT NULL REFERENCES cases(case_id),
  image_type TEXT,
  file_path TEXT NOT NULL,
  original_filename TEXT,
  acquisition_year INTEGER,
  acquisition_period TEXT,
  device TEXT,
  width INTEGER,
  height INTEGER,
  illumination TEXT,
  approximate_distance TEXT,
  has_scale BOOLEAN,
  quality_score TEXT,
  duplicate_group_id TEXT,
  leakage_risk BOOLEAN DEFAULT false,
  anonymization_status TEXT,
  has_identifying_risk BOOLEAN DEFAULT false,
  sha256 TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE pathology_reports (
  report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID NOT NULL REFERENCES cases(case_id),
  pathology_number_hash TEXT,
  report_date DATE,
  biopsy_relative_date TEXT,
  histological_diagnosis TEXT,
  histological_type TEXT,
  subtype TEXT,
  margins TEXT,
  breslow_mm NUMERIC,
  clark_level TEXT,
  ulceration BOOLEAN,
  mitotic_index TEXT,
  perineural_invasion BOOLEAN,
  immunohistochemistry TEXT,
  full_text_redacted TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE surgical_procedures (
  procedure_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID NOT NULL REFERENCES cases(case_id),
  procedure_type TEXT,
  procedure_date DATE,
  body_site TEXT,
  surgical_margins_planned TEXT,
  specimen_id_hash TEXT,
  surgeon_id_hash TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE expert_reviews (
  review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID NOT NULL REFERENCES cases(case_id),
  reviewer_id_hash TEXT,
  reviewer_specialty TEXT,
  diagnosis TEXT,
  consensus_diagnosis TEXT,
  confidence_score INTEGER CHECK (confidence_score BETWEEN 1 AND 5),
  image_quality INTEGER CHECK (image_quality BETWEEN 1 AND 5),
  agreement_level TEXT,
  review_status TEXT,
  reviewed_at TIMESTAMP DEFAULT now()
);

CREATE TABLE annotations (
  annotation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  image_id UUID NOT NULL REFERENCES images(image_id),
  annotation_type TEXT,
  annotation_json JSONB,
  annotator_id_hash TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE clinical_followups (
  followup_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID NOT NULL REFERENCES cases(case_id),
  followup_date DATE,
  recurrence BOOLEAN,
  progression BOOLEAN,
  metastasis BOOLEAN,
  treatment_response TEXT,
  outcome_status TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE quality_audits (
  audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  target_type TEXT CHECK (target_type IN ('patient', 'case', 'image', 'pathology_report', 'split', 'dataset_version')),
  target_id TEXT NOT NULL,
  audit_type TEXT,
  audit_status TEXT,
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  reviewer_id_hash TEXT,
  reviewed_at TIMESTAMP DEFAULT now(),
  remediation_action TEXT,
  notes TEXT
);

CREATE TABLE consents_ethics (
  ethics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID REFERENCES cases(case_id),
  cep_approval TEXT,
  consent_status TEXT,
  consent_waiver BOOLEAN,
  data_use_agreement TEXT,
  access_policy TEXT,
  reidentification_prohibited BOOLEAN DEFAULT true,
  redistribution_prohibited BOOLEAN DEFAULT true,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE dataset_splits (
  split_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(patient_id),
  split TEXT CHECK (split IN ('train', 'validation', 'test')) NOT NULL,
  dataset_version TEXT,
  created_at TIMESTAMP DEFAULT now(),
  UNIQUE (patient_id, dataset_version)
);

CREATE INDEX idx_cases_patient_id ON cases(patient_id);
CREATE INDEX idx_images_case_id ON images(case_id);
CREATE INDEX idx_surgical_procedures_case_id ON surgical_procedures(case_id);
CREATE INDEX idx_pathology_reports_case_id ON pathology_reports(case_id);
CREATE INDEX idx_expert_reviews_case_id ON expert_reviews(case_id);
CREATE INDEX idx_annotations_image_id ON annotations(image_id);
CREATE INDEX idx_clinical_followups_case_id ON clinical_followups(case_id);
CREATE INDEX idx_quality_audits_target ON quality_audits(target_type, target_id);
CREATE INDEX idx_images_sha256 ON images(sha256);
CREATE INDEX idx_cases_evidence_level ON cases(evidence_level);
CREATE INDEX idx_dataset_splits_split ON dataset_splits(split);
