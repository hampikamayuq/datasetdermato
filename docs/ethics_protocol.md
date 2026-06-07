# Ethics Protocol

## Governance fields

Track the following for institutional datasets:

- CEP approval
- consent status
- waiver of consent, when applicable
- dataset terms of use
- data use agreement
- access policy
- prohibition of reidentification
- prohibition of unauthorized redistribution

## Recommended access classes

- `internal_research`: local research only
- `controlled_access`: available after review and agreement
- `public_metadata_only`: metadata may be public, images restricted
- `public_release`: images and metadata may be released

## Identifiers

Never store raw patient identifiers in dataset files.

Use separate identifiers:

- `patient_id`
- `patient_hash`
- `case_id`
- `lesion_id`
- `image_id`
- `pathology_report_id`

The same patient must never appear in more than one train/validation/test split.

## De-identification

Minimum steps:

- remove EXIF metadata
- remove names, record numbers, dates, and labels
- review faces, tattoos, and unique contextual details
- mark images with possible identifying risk

## LGPD note

Health images and linked clinical metadata should be treated as sensitive personal data. Any release must be reviewed under the institution's ethics and legal governance.

## Brazil research governance

For Brazilian research settings, align the project with:

- CNS Resolution 466/2012 for the general ethical framework of research involving human participants.
- CNS Resolution 738/2024 for scientific research databases involving human participants.
- Local CEP/CONEP guidance for use, reuse, sharing, and repository deposition of anonymized or sensitive databases.

Dataset release should distinguish:

- anonymized public metadata
- controlled-access images
- sensitive or identifiable data that must remain restricted
- reuse scenarios requiring new ethics review
