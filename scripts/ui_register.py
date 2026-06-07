"""Visual image registration tool.

Run with:
    streamlit run scripts/ui_register.py
"""

from __future__ import annotations

import csv
import sys
import tempfile
from datetime import date
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))

from ingest_image import file_sha256, hash_identifier, make_uuid, remove_exif

MANIFEST = REPO_ROOT / "metadata" / "dataset_manifest.csv"
CORE_META = REPO_ROOT / "metadata" / "standardized" / "core_metadata_template.csv"
PROCESSED_DIR = REPO_ROOT / "data" / "processed" / "images"
SOURCE_CATALOG = REPO_ROOT / "metadata" / "sources" / "source_catalog.csv"
TAXONOMY = REPO_ROOT / "annotations" / "labels" / "taxonomy.csv"

IMAGE_TYPES = [
    "dermoscopic",
    "clinical: overview",
    "clinical: close-up",
    "TBP tile: close-up",
    "TBP tile: overview",
]

SPECIALTY_OPTIONS = [
    "",
    "general_dermatology",
    "pediatric_dermatology",
    "dermatologic_surgery",
    "dermatopathology",
    "oncologic_dermatology",
    "trichology",
    "hanseniasis",
    "autoimmune_skin_disease",
    "contact_dermatitis",
    "pigmented_lesions",
    "inflammatory_skin_disease",
    "infectious_dermatology",
    "tropical_dermatology",
    "cutaneous_tumors",
    "dermoscopy",
]


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def _load_source_ids() -> list[str]:
    if not SOURCE_CATALOG.exists():
        return []
    with SOURCE_CATALOG.open(newline="", encoding="utf-8") as fh:
        return [row["source_id"] for row in csv.DictReader(fh) if row.get("source_id")]


def _load_diagnoses() -> list[str]:
    if not TAXONOMY.exists():
        return []
    with TAXONOMY.open(newline="", encoding="utf-8") as fh:
        return [row["label_name"] for row in csv.DictReader(fh) if row.get("label_name")]


def _known_sha256s() -> set[str]:
    if not MANIFEST.exists() or MANIFEST.stat().st_size == 0:
        return set()
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return {row["sha256"] for row in csv.DictReader(fh) if row.get("sha256")}


def _append_row(csv_path: Path, row: dict) -> None:
    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()), extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


# ---------------------------------------------------------------------------
# Registration logic (same as CLI)
# ---------------------------------------------------------------------------

def register_image(
    tmp_src: Path,
    original_name: str,
    source_id: str,
    image_type: str,
    diagnosis: str,
    patient_id: str,
    lesion_id: str,
    case_id: str,
    specialty: str,
    source_url: str,
    notes: str,
) -> dict:
    src_hash = file_sha256(tmp_src)
    if src_hash in _known_sha256s():
        raise ValueError(f"Duplicata: SHA256 {src_hash[:16]}… já existe no manifesto.")

    suffix = Path(original_name).suffix or ".jpg"
    image_id = make_uuid()
    slug = diagnosis.lower().replace(" ", "_")
    out_name = f"{source_id}_{slug}_{image_id[:8]}{suffix}"
    out_path = PROCESSED_DIR / out_name
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    width, height = remove_exif(tmp_src, out_path)
    processed_hash = file_sha256(out_path)
    patient_hash = hash_identifier(patient_id, source_id) if patient_id else ""

    manifest_row = {
        "image_id": image_id,
        "filename": str(out_path.relative_to(REPO_ROOT)),
        "source_id": source_id,
        "source_type": "",
        "specialty_service": specialty,
        "source_image_url": source_url,
        "source_page_url": "",
        "source_license_status": "pending",
        "attribution": "",
        "accessed_at": str(date.today()),
        "sha256": processed_hash,
        "width": width,
        "height": height,
        "image_type": image_type,
        "diagnosis_original": diagnosis,
        "diagnosis_normalized": diagnosis,
        "label_id": slug,
        "patient_id": patient_hash,
        "lesion_id": lesion_id,
        "split": "",
        "quality_status": "pending",
        "review_status": "pending",
        "notes": notes,
    }
    _append_row(MANIFEST, manifest_row)

    core_row = {
        "filename": manifest_row["filename"],
        "image_type": image_type,
        "dermoscopic_type": "",
        "tbp_tile_type": "",
        "age": "",
        "sex": "",
        "anatom_site_general": "",
        "anatom_site_special": "",
        "fitzpatrick_skin_type": "",
        "acquisition_day": "",
        "personal_hx_mm": "",
        "family_hx_mm": "",
        "lesion_id": lesion_id,
        "patient_id": patient_hash,
        "rcm_case_id": case_id,
        "clin_size_long_diam_mm": "",
        "diagnosis": diagnosis,
        "benign_malignant": "",
        "concomitant_biopsy": "",
        "diagnosis_confirm_type": "",
        "melanocytic": "",
        "nevus_type": "",
        "mel_thick_mm": "",
        "mel_class": "",
        "mel_type": "",
        "mel_mitotic_index": "",
        "mel_ulcer": "",
    }
    _append_row(CORE_META, core_row)

    return {
        "image_id": image_id,
        "filename": manifest_row["filename"],
        "sha256": processed_hash,
        "width": width,
        "height": height,
    }


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def _manifest_preview() -> None:
    if not MANIFEST.exists() or MANIFEST.stat().st_size == 0:
        st.info("Nenhuma imagem registrada ainda.")
        return
    import pandas as pd
    df = pd.read_csv(MANIFEST)
    cols = ["image_id", "filename", "source_id", "image_type", "diagnosis_original",
            "quality_status", "accessed_at"]
    st.dataframe(df[[c for c in cols if c in df.columns]], use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Registro de Imagens", layout="wide")
    st.title("Registro de Imagens Dermatológicas")

    source_ids = _load_source_ids()
    diagnoses = _load_diagnoses()

    tab_register, tab_manifest = st.tabs(["Registrar imagem", "Manifesto"])

    # ------------------------------------------------------------------
    # Tab: Register
    # ------------------------------------------------------------------
    with tab_register:
        col_img, col_form = st.columns([1, 1], gap="large")

        with col_img:
            uploaded = st.file_uploader(
                "Selecione a imagem",
                type=["jpg", "jpeg", "png", "bmp", "tif", "tiff"],
            )
            if uploaded:
                st.image(uploaded, use_container_width=True)
                st.caption(f"Arquivo: {uploaded.name}  |  {uploaded.size // 1024} KB")

        with col_form:
            st.subheader("Metadados")

            source_id = st.selectbox(
                "Fonte (source_id) *",
                options=source_ids if source_ids else [""],
                help="Cadastre a fonte em metadata/sources/source_catalog.csv",
            )

            image_type = st.selectbox("Tipo de imagem *", IMAGE_TYPES)

            diagnosis_input = st.selectbox(
                "Diagnóstico *",
                options=[""] + diagnoses,
                help="Selecione da taxonomia ou digite abaixo",
            )
            diagnosis_free = st.text_input(
                "Diagnóstico livre (sobrescreve seleção acima se preenchido)"
            )
            diagnosis = diagnosis_free.strip() or diagnosis_input.strip()

            st.divider()
            st.subheader("Identificadores (opcionais)")

            patient_id = st.text_input(
                "ID do paciente",
                help="Será convertido em hash antes de salvar",
            )
            lesion_id = st.text_input("ID da lesão")
            case_id = st.text_input("UUID do caso (se já existir)")

            st.divider()
            st.subheader("Contexto clínico (opcional)")

            specialty = st.selectbox("Subespecialidade", SPECIALTY_OPTIONS)
            source_url = st.text_input("URL de origem da imagem")
            notes = st.text_area("Notas", height=80)

            submitted = st.button("Registrar imagem", type="primary", disabled=not uploaded)

            if submitted and uploaded:
                if not source_id:
                    st.error("Selecione uma fonte.")
                elif not diagnosis:
                    st.error("Informe o diagnóstico.")
                else:
                    with tempfile.NamedTemporaryFile(
                        suffix=Path(uploaded.name).suffix, delete=False
                    ) as tmp:
                        tmp.write(uploaded.getbuffer())
                        tmp_path = Path(tmp.name)

                    try:
                        result = register_image(
                            tmp_src=tmp_path,
                            original_name=uploaded.name,
                            source_id=source_id,
                            image_type=image_type,
                            diagnosis=diagnosis,
                            patient_id=patient_id,
                            lesion_id=lesion_id,
                            case_id=case_id,
                            specialty=specialty,
                            source_url=source_url,
                            notes=notes,
                        )
                        st.success("Imagem registrada com sucesso.")
                        st.json(result)
                    except ValueError as exc:
                        st.error(str(exc))
                    finally:
                        tmp_path.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Tab: Manifest
    # ------------------------------------------------------------------
    with tab_manifest:
        st.subheader("Imagens registradas")
        if st.button("Atualizar"):
            st.rerun()
        _manifest_preview()


if __name__ == "__main__":
    main()
