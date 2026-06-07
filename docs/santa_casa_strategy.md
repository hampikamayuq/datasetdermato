# Santa Casa Dataset Strategy

## Principle

The core asset is not the photo collection. The core asset is the documented clinical case.

For a historical dermatology archive, especially one that may go back to 1998, the strongest strategy is to start from cases with diagnostic evidence and then link images to those cases.

## Priority 1: Anatomic pathology

Start with pathology records when possible.

```text
pathology report
  -> case identification
  -> medical record lookup
  -> clinical or dermoscopy image lookup
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
```

## Priority 2: Professor and assistant archives

Faculty archives are likely easier to recover than old resident phone collections.

Potential advantages:

- fewer people to contact
- larger stable collections per person
- better longitudinal follow-up
- more interesting or rare cases
- better diagnostic confidence

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

## Priority 4: Residents

Resident image recovery should be a later phase.

Expected issues:

- high dispersion
- lost files
- changed phones
- heterogeneous image quality
- inconsistent metadata
- weak linkage to pathology or follow-up

## Evidence levels

Use three dataset tiers:

| Level | Definition | Typical evidence |
| --- | --- | --- |
| Bronze | Clinical image plus original care diagnosis | assistential diagnosis |
| Silver | Clinical image plus specialist review | expert review or consensus |
| Gold | Clinical image plus histopathology and expert review | pathology-confirmed diagnosis |

## Suggested scale

Targets should be treated as long-term goals:

- Gold: 10,000 to 50,000 cases
- Silver: 50,000 to 200,000 cases
- Bronze: hundreds of thousands of cases, if governance allows

## Institutional advantage

Santa Casa may have a rare chain:

```text
clinical care
  -> dermoscopy
  -> dermatologic surgery
  -> pathology
  -> follow-up
```

A dataset with this chain is scientifically stronger than a large collection of disconnected images.
