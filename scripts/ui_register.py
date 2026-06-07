"""Visual dataset curation tool.

Run with:
    streamlit run scripts/ui_register.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from dataset_constants import SOURCE_CATALOG
from dataset_ops import (
    IMAGE_TYPES,
    MANIFEST,
    SOURCE_TYPE_OPTIONS,
    SPECIALTY_OPTIONS,
    load_diagnoses,
    load_source_ids,
    register_image_file,
)
from dataset_validate import validate_all


def manifest_preview() -> None:
    if not MANIFEST.exists() or MANIFEST.stat().st_size == 0:
        st.info("No registered images yet.")
        return

    df = pd.read_csv(MANIFEST)
    if df.empty:
        st.info("No registered images yet.")
        return

    metric_cols = st.columns(4)
    metric_cols[0].metric("Images", len(df))
    metric_cols[1].metric("Sources", df["source_id"].nunique() if "source_id" in df else 0)
    metric_cols[2].metric("Pending quality", int((df.get("quality_status") == "pending").sum()) if "quality_status" in df else 0)
    metric_cols[3].metric("Pending review", int((df.get("review_status") == "pending").sum()) if "review_status" in df else 0)

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


def validation_panel() -> None:
    if st.button("Run validation", type="primary"):
        st.session_state["validation_results"] = validate_all()

    results = st.session_state.get("validation_results")
    if not results:
        st.info("Validation has not run yet.")
        return

    total_errors = sum(len(result.errors) for result in results)
    total_warnings = sum(len(result.warnings) for result in results)

    metric_cols = st.columns(3)
    metric_cols[0].metric("Checks", len(results))
    metric_cols[1].metric("Errors", total_errors)
    metric_cols[2].metric("Warnings", total_warnings)

    for result in results:
        if result.ok:
            st.success(f"{result.name}: passed")
        else:
            st.error(f"{result.name}: {len(result.errors)} error(s)")
        if result.warnings:
            st.warning("\n".join(result.warnings))
        if result.errors:
            st.code("\n".join(result.errors), language="text")


def sources_panel() -> None:
    if not SOURCE_CATALOG.exists() or SOURCE_CATALOG.stat().st_size == 0:
        st.info("No source catalog found.")
        return

    df = pd.read_csv(SOURCE_CATALOG)
    if df.empty:
        st.info("No sources registered yet.")
        return

    metric_cols = st.columns(3)
    metric_cols[0].metric("Sources", len(df))
    metric_cols[1].metric(
        "Controlled access",
        int((df.get("access_type") == "controlled access").sum()) if "access_type" in df else 0,
    )
    metric_cols[2].metric(
        "Verify redistribution",
        int(df.get("redistribution_status", pd.Series(dtype=str)).astype(str).str.contains("verify", case=False, na=False).sum())
        if "redistribution_status" in df
        else 0,
    )
    st.dataframe(df, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Dermatology Dataset Curation", layout="wide")
    st.title("Dermatology Dataset Curation")

    source_ids = load_source_ids()
    diagnoses = load_diagnoses()

    tab_register, tab_validation, tab_manifest, tab_sources = st.tabs(
        ["Register image", "Validation", "Manifest", "Sources"]
    )

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

    with tab_validation:
        st.subheader("Dataset validation")
        validation_panel()

    with tab_sources:
        st.subheader("Source catalog")
        sources_panel()


if __name__ == "__main__":
    main()
