# Annotation Protocol

## Annotation types

Supported annotation types:

- `bbox`: bounding box around lesion
- `mask`: pixel-level lesion mask
- `polygon`: polygon around lesion or region of interest
- `exclude_region`: region that should not be used for model training
- `multi_lesion`: multiple lesion annotations in the same image

## Minimum annotation record

Each annotation must link to one image:

- `annotation_id`
- `image_id`
- `annotation_type`
- `annotation_json`
- `annotator_id_hash`
- `created_at`

## JSON examples

Bounding box:

```json
{
  "x": 120,
  "y": 80,
  "width": 260,
  "height": 210
}
```

Polygon:

```json
{
  "points": [
    [120, 80],
    [260, 90],
    [300, 220],
    [140, 240]
  ]
}
```

Mask:

```json
{
  "mask_path": "annotations/masks/example_0001.png",
  "format": "binary_png"
}
```

## Review

Recommended review statuses:

- `unreviewed`
- `single_annotator`
- `double_annotator`
- `expert_corrected`
- `consensus_final`

## Exclusion regions

Use exclusion regions for:

- faces
- identifying tattoos
- hospital labels
- rulers or labels with patient data
- irrelevant image borders
