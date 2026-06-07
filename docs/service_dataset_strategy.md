# Dermatology Service Dataset Strategy

## Principle

The core asset is not the photo collection. The core asset is the documented clinical case.

For a retrospective dermatology archive, especially one beginning in the 1990s or earlier, the strongest strategy is to start from cases with diagnostic evidence and then link images to those cases.

## Priority 1: Anatomic pathology

Start with pathology records when possible.

```text
pathology report
  -> case identification
  -> medical record lookup
  -> clinical, dermoscopic, surgical, or histopathology image lookup
  -> image + report linkage
```

Why this matters:

- histopathology provides high-quality ground truth
- labels are less noisy
- the dataset becomes more valuable for AI research
- publications become more defensible

Example:

```text
2004
nodular basal cell carcinoma
pathology report available
clinical photo available
evidence_level = gold
source_type = pathology_archive
specialty_service = oncologic_dermatology
```

## Priority 2: Faculty and assistant archives

Faculty archives are often easier to recover than old resident phone collections.

Potential advantages:

- fewer people to contact
- larger stable collections per person
- better longitudinal follow-up
- more interesting or rare cases
- better diagnostic confidence

Use `source_type = faculty_collection` for these records.

## Priority 3: Pathology books, lectures, and presentations

Useful sources:

- lectures
- seminars
- conference presentations
- PowerPoint archives
- old CDs
- laboratory hard drives
- pathology teaching files

These may already link clinical images with confirmed diagnoses.

Use `source_type = conference_archive` or `pathology_archive`, depending on provenance.

## Priority 4: Residents

Resident image recovery should be a later phase.

Expected issues:

- high dispersion
- lost files
- changed phones
- heterogeneous image quality
- inconsistent metadata
- weak linkage to pathology or follow-up

Use `source_type = resident_collection` when these archives are incorporated.

## Evidence levels

Use three dataset tiers:

| Level | Definition | Typical evidence |
| --- | --- | --- |
| Bronze | Clinical image plus original care diagnosis | assistential diagnosis |
| Silver | Clinical image plus specialist review | expert review or consensus |
| Gold | Clinical image plus histopathology and expert review | pathology-confirmed diagnosis |

## Source types

Allowed `source_type` values:

- `faculty_collection`
- `resident_collection`
- `pathology_archive`
- `clinical_archive`
- `conference_archive`
- `research_project`
- `private_practice_archive`
- `institutional_database`

## Specialty services

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

## Scientific advantage

A dermatology service may have a rare chain:

```text
clinical care
  -> dermoscopy
  -> dermatologic surgery
  -> pathology
  -> expert review
  -> follow-up
```

A dataset with this chain is scientifically stronger than a large collection of disconnected images.

The project should support retrospective archives accumulated through care, teaching, research, faculty collections, pathology laboratories, historical archives, scientific presentations, and institutional systems.
