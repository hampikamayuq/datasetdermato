"""Visual image registration tool.

Run with:
    streamlit run scripts/ui_register.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from dataset_ops import (
    IMAGE_TYPES,
    MANIFEST,
    SOURCE_TYPE_OPTIONS,
    SPECIALTY_OPTIONS,
    load_diagnoses,
    load_source_ids,
    register_image_file,
)


def manifest_preview() -> None:
    if not MANIFEST.exists() or MANIFEST.stat().st_size == 0:
        st.info("No registered images yet.")
        return

    df = pd.read_csv(MANIFEST)
    cols = [
        "image_id",
        "filename",
        "source_id",
        "source_type",
        "specialty_service",
        "image_type",
        "diagnosis_original",
        "quality_status",
        "accessed_at",
    ]
    st.dataframe(df[[c for c in cols if c in df.columns]], use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Dermatology Image Registration", layout="wide")
    st.title("Dermatology Image Registration")

    source_ids = load_source_ids()
    diagnoses = load_diagnoses()

    tab_register, tab_manifest = st.tabs(["Register image", "Manifest"])

    with tab_register:
        col_img, col_form = st.columns([1, 1], gap="large")

        with col_img:
            uploaded = st.file_uploader(
                "Select image",
                type=["jpg", "jpeg", "png", "bmp", "tif", "tiff"],
            )
            if uploaded:
                st.image(uploaded, use_container_width=True)
                st.caption(f"File: {uploaded.name} | {uploaded.size // 1024} KB")

        with col_form:
            st.subheader("Required metadata")
            source_id = st.selectbox("Source ID", options=source_ids if source_ids else [""])
            image_type = st.selectbox("Image type", IMAGE_TYPES)

            diagnosis_selected = st.selectbox("Diagnosis", options=[""] + diagnoses)
            diagnosis_free = st.text_input("Free-text diagnosis")
            diagnosis = diagnosis_free.strip() or diagnosis_selected.strip()

            st.subheader("Optional identifiers")
            patient_id = st.text_input("Patient ID", help="Saved only as a salted hash")
            lesion_id = st.text_input("Lesion ID")
            case_id = st.text_input("Case UUID")

            st.subheader("Context")
            source_type = st.selectbox("Source type", SOURCE_TYPE_OPTIONS)
            specialty_service = st.selectbox("Specialty service", SPECIALTY_OPTIONS)
            source_url = st.text_input("Source image URL")
            notes = st.text_area("Notes", height=80)

            submitted = st.button("Register image", type="primary", disabled=not uploaded)

            if submitted and uploaded:
                if not source_id:
                    st.error("Select a source ID.")
                elif not diagnosis:
                    st.error("Enter a diagnosis.")
                else:
                    with tempfile.NamedTemporaryFile(
                        suffix=Path(uploaded.name).suffix, delete=False
                    ) as temp_file:
                        temp_file.write(uploaded.getbuffer())
                        temp_path = Path(temp_file.name)

                    try:
                        result = register_image_file(
                            input_path=temp_path,
                            source_id=source_id,
                            image_type=image_type,
                            diagnosis=diagnosis,
                            patient_id=patient_id,
                            lesion_id=lesion_id,
                            case_id=case_id,
                            source_type=source_type,
                            specialty_service=specialty_service,
                            source_url=source_url,
                            notes=notes,
                            original_name=uploaded.name,
                        )
                        st.success("Image registered.")
                        st.json(result)
                    except (FileNotFoundError, ValueError) as exc:
                        st.error(str(exc))
                    finally:
                        temp_path.unlink(missing_ok=True)

    with tab_manifest:
        st.subheader("Registered images")
        if st.button("Refresh"):
            st.rerun()
        manifest_preview()


if __name__ == "__main__":
    main()
