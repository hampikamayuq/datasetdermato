# Literature Review and Design Implications

This file summarizes reference works that inform the design of `dermatology-service-dataset`.

## Dermatology AI and datasets

### Esteva et al., 2017

The Nature study on dermatologist-level skin cancer classification established the importance of large-scale image datasets, specialist comparison, and clinically meaningful binary or hierarchical tasks.

Applied design choices:

- keep diagnostic hierarchy fields (`diagnosis_primary`, `diagnosis_group`, `benign_malignant`)
- track expert review separately from original diagnosis
- preserve evidence level (`bronze`, `silver`, `gold`)

### Tschandl et al., 2018: HAM10000

HAM10000 is a key dermoscopy benchmark with multi-source images and defined diagnostic classes.

Applied design choices:

- track source and provenance explicitly
- support dermoscopy-specific metadata
- preserve class labels in a normalized taxonomy

### ISIC Archive

ISIC is a reference for dermatology image metadata, contribution workflows, and de-identification behavior.

Applied design choices:

- keep a standardized image-level metadata template
- preserve lesion and patient identifiers as mapped or hashed identifiers
- support externally inspired but project-specific validation rules

### Daneshjou et al., 2022: DDI

DDI emphasizes diverse skin tones, expert curation, and pathology-confirmed labels.

Applied design choices:

- track skin type and demographic subgroup fields
- support pathology-confirmed `gold` cases
- require fairness and subgroup performance reporting

### Groh et al., 2021: Fitzpatrick17k

Fitzpatrick17k highlights clinical dermatology images with Fitzpatrick skin type annotations and fairness evaluation.

Applied design choices:

- require Fitzpatrick or equivalent skin tone documentation when ethically available
- track performance by skin tone, diagnosis, source type, and specialty service

### DERM12345, 2024

DERM12345 is useful as a model for describing a multisource dermoscopy dataset with patient count, acquisition period, subclasses, and technical acquisition context.

Applied design choices:

- document patient count separately from image count
- record acquisition period and source count
- maintain dataset versioning and descriptive statistics

## Dataset quality and documentation

### Gebru et al., 2021: Datasheets for Datasets

Datasheets motivate structured documentation of motivation, composition, collection process, preprocessing, uses, distribution, maintenance, and limitations.

Applied design choices:

- add a dataset datasheet template
- require intended and out-of-scope uses
- document maintenance, access, and limitations

### Dermatology dataset quality audits

Recent evaluations of dermatology datasets emphasize duplicate images, train/test leakage, incorrect labels, missing partitions, and irrelevant samples.

Applied design choices:

- add `metadata/audits/quality_audit.csv`
- require patient-level splits
- track duplicate, label, leakage, and image-quality flags

### Skin type diversity reviews

Reviews of skin tone diversity in dermatology datasets show the need to document representativeness and subgroup performance.

Applied design choices:

- add a fairness and bias plan
- track subgroup coverage by skin tone, age, sex, geography, body site, source type, and specialty service

## AI medical reporting guidelines

### TRIPOD+AI

Use TRIPOD+AI when reporting development or validation of prediction models using regression or machine learning.

### CONSORT-AI

Use CONSORT-AI for clinical trials evaluating AI interventions.

### STARD-AI

Use STARD-AI for diagnostic accuracy studies involving AI systems.

Applied design choices:

- add a publication checklist
- separate dataset release from model validation
- require explicit target population, reference standard, and subgroup evaluation

## Brazil ethics and governance

### CNS Resolution 466/2012

Use as the broad ethical framework for research involving human participants in Brazil.

### CNS Resolution 738/2024

Use for research databases involving human participants, including governance of scientific data banks and possible consent waiver scenarios.

### CEP/Fiocruz guidance on database use

Use as operational guidance for anonymized data, sensitive data, repository sharing, reuse, and CEP/CONEP review.

Applied design choices:

- keep `consents_ethics.csv`
- document access classes
- separate internal research, controlled access, public metadata, and public release
- require ethics approval or documented waiver before release
