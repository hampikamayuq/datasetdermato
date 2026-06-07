"""Visual dataset curation app.

Run with:
    streamlit run scripts/dataset_app.py
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


PAGES = ["Painel", "Registrar imagem", "Validacao", "Manifesto", "Fontes"]

SOURCE_COLUMNS = [
    "source_id",
    "source_name",
    "homepage_url",
    "source_type",
    "access_type",
    "redistribution_status",
    "license_or_terms_url",
    "notes",
]


def read_table(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=columns or [])

    df = pd.read_csv(path, dtype=str).fillna("")
    if columns:
        for column in columns:
            if column not in df.columns:
                df[column] = ""
        extra_columns = [column for column in df.columns if column not in columns]
        df = df[columns + extra_columns]
    return df


def save_table(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.fillna("").to_csv(path, index=False, lineterminator="\n")


def manifest_df() -> pd.DataFrame:
    return read_table(MANIFEST)


def sources_df() -> pd.DataFrame:
    return read_table(SOURCE_CATALOG, SOURCE_COLUMNS)


def validation_results(force: bool = False):
    if force or "validation_results" not in st.session_state:
        st.session_state["validation_results"] = validate_all()
    return st.session_state["validation_results"]


def validation_counts(results) -> tuple[int, int]:
    errors = sum(len(result.errors) for result in results)
    warnings = sum(len(result.warnings) for result in results)
    return errors, warnings


def navigate(page: str) -> None:
    st.session_state["page"] = page
    st.rerun()


def sidebar() -> str:
    if "page" not in st.session_state:
        st.session_state["page"] = PAGES[0]

    current_page = st.session_state["page"]
    page = st.sidebar.radio(
        "Navegacao",
        PAGES,
        index=PAGES.index(current_page) if current_page in PAGES else 0,
    )
    st.session_state["page"] = page

    st.sidebar.divider()
    if st.sidebar.button("Validar agora", use_container_width=True):
        validation_results(force=True)
        st.session_state["page"] = "Validacao"
        st.rerun()
    if st.sidebar.button("Nova imagem", use_container_width=True):
        navigate("Registrar imagem")

    return page


def status_label(ok: bool) -> str:
    return "OK" if ok else "Pendente"


def dashboard_page() -> None:
    st.title("Dermatology Dataset")

    manifest = manifest_df()
    sources = sources_df()
    results = validation_results()
    errors, warnings = validation_counts(results)

    image_count = len(manifest)
    source_count = len(sources)
    pending_quality = (
        int((manifest["quality_status"] == "pending").sum())
        if "quality_status" in manifest.columns and not manifest.empty
        else 0
    )

    metric_cols = st.columns(4)
    metric_cols[0].metric("Imagens", image_count)
    metric_cols[1].metric("Fontes", source_count)
    metric_cols[2].metric("Erros", errors)
    metric_cols[3].metric("Pendencias", pending_quality + warnings)

    steps = [
        ("Fontes cadastradas", source_count > 0),
        ("Imagens registradas", image_count > 0),
        ("Validacao sem erro", errors == 0),
        ("Qualidade revisada", image_count > 0 and pending_quality == 0),
    ]
    progress = sum(1 for _, done in steps if done) / len(steps)
    st.progress(progress)

    step_cols = st.columns(len(steps))
    for column, (label, done) in zip(step_cols, steps):
        column.metric(label, status_label(done))

    st.divider()

    action_cols = st.columns(4)
    if action_cols[0].button("Cadastrar fonte", use_container_width=True):
        navigate("Fontes")
    if action_cols[1].button("Registrar imagem", use_container_width=True):
        navigate("Registrar imagem")
    if action_cols[2].button("Validar dataset", use_container_width=True):
        validation_results(force=True)
        navigate("Validacao")
    if action_cols[3].button("Ver manifesto", use_container_width=True):
        navigate("Manifesto")

    st.divider()

    if manifest.empty:
        st.info("Nenhuma imagem registrada.")
    else:
        st.subheader("Ultimos registros")
        preview_columns = [
            "filename",
            "source_id",
            "image_type",
            "diagnosis_original",
            "quality_status",
            "accessed_at",
        ]
        available_columns = [column for column in preview_columns if column in manifest.columns]
        st.dataframe(manifest.tail(8)[available_columns], use_container_width=True)


def register_page() -> None:
    st.title("Registrar imagem")

    source_ids = load_source_ids()
    diagnoses = load_diagnoses()

    if not source_ids:
        st.warning("Cadastre uma fonte antes de registrar imagens.")
        if st.button("Abrir fontes"):
            navigate("Fontes")
        return

    col_img, col_form = st.columns([1, 1], gap="large")

    with col_img:
        uploaded = st.file_uploader(
            "Imagem",
            type=["jpg", "jpeg", "png", "bmp", "tif", "tiff"],
        )
        if uploaded:
            st.image(uploaded, use_container_width=True)
            st.caption(f"{uploaded.name} | {uploaded.size // 1024} KB")

    with col_form:
        source_id = st.selectbox("Fonte", options=source_ids)
        image_type = st.selectbox("Tipo de imagem", IMAGE_TYPES)

        diagnosis_selected = st.selectbox("Diagnostico padronizado", options=[""] + diagnoses)
        diagnosis_free = st.text_input("Diagnostico livre")
        diagnosis = diagnosis_free.strip() or diagnosis_selected.strip()

        with st.expander("Identificadores", expanded=False):
            patient_id = st.text_input("Paciente", help="Sera salvo apenas como hash")
            lesion_id = st.text_input("Lesao")
            case_id = st.text_input("Caso")

        with st.expander("Contexto", expanded=False):
            source_type = st.selectbox("Origem do caso", SOURCE_TYPE_OPTIONS)
            specialty_service = st.selectbox("Servico", SPECIALTY_OPTIONS)
            source_url = st.text_input("URL da imagem")
            notes = st.text_area("Notas", height=80)

        submitted = st.button(
            "Registrar",
            type="primary",
            disabled=not uploaded,
            use_container_width=True,
        )

        if submitted and uploaded:
            if not diagnosis:
                st.error("Informe um diagnostico.")
                return

            with tempfile.NamedTemporaryFile(suffix=Path(uploaded.name).suffix, delete=False) as temp_file:
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
                st.session_state.pop("validation_results", None)
                st.success("Imagem registrada.")
                st.json(result)
            except (FileNotFoundError, ValueError) as exc:
                st.error(str(exc))
            finally:
                temp_path.unlink(missing_ok=True)


def validation_page() -> None:
    st.title("Validacao")

    col_run, col_status = st.columns([1, 3])
    if col_run.button("Executar", type="primary", use_container_width=True):
        results = validation_results(force=True)
    else:
        results = validation_results()

    errors, warnings = validation_counts(results)
    col_status.metric("Erros", errors)

    summary = [
        {
            "grupo": result.name,
            "status": "OK" if result.ok else "Erro",
            "erros": len(result.errors),
            "avisos": len(result.warnings),
        }
        for result in results
    ]
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

    for result in results:
        if result.errors:
            with st.expander(f"{result.name}: erros", expanded=True):
                st.code("\n".join(result.errors), language="text")
        if result.warnings:
            with st.expander(f"{result.name}: avisos", expanded=False):
                st.code("\n".join(result.warnings), language="text")


def manifest_page() -> None:
    st.title("Manifesto")

    df = manifest_df()
    if df.empty:
        st.info("Nenhuma imagem registrada.")
        return

    filters = st.columns(4)
    source = filters[0].selectbox("Fonte", ["Todas"] + sorted(df.get("source_id", pd.Series(dtype=str)).unique()))
    image_type = filters[1].selectbox(
        "Tipo",
        ["Todos"] + sorted(df.get("image_type", pd.Series(dtype=str)).unique()),
    )
    quality = filters[2].selectbox(
        "Qualidade",
        ["Todas"] + sorted(df.get("quality_status", pd.Series(dtype=str)).unique()),
    )
    search = filters[3].text_input("Buscar")

    filtered = df.copy()
    if source != "Todas" and "source_id" in filtered.columns:
        filtered = filtered[filtered["source_id"] == source]
    if image_type != "Todos" and "image_type" in filtered.columns:
        filtered = filtered[filtered["image_type"] == image_type]
    if quality != "Todas" and "quality_status" in filtered.columns:
        filtered = filtered[filtered["quality_status"] == quality]
    if search:
        haystack = filtered.astype(str).agg(" ".join, axis=1).str.lower()
        filtered = filtered[haystack.str.contains(search.lower(), na=False)]

    metric_cols = st.columns(3)
    metric_cols[0].metric("Registros", len(filtered))
    metric_cols[1].metric("Total", len(df))
    metric_cols[2].metric("Fontes", filtered["source_id"].nunique() if "source_id" in filtered else 0)

    preferred_columns = [
        "image_id",
        "filename",
        "source_id",
        "source_type",
        "specialty_service",
        "image_type",
        "diagnosis_original",
        "quality_status",
        "review_status",
        "accessed_at",
    ]
    columns = [column for column in preferred_columns if column in filtered.columns]
    st.dataframe(filtered[columns], use_container_width=True, height=520)

    st.download_button(
        "Baixar manifesto filtrado",
        data=filtered.to_csv(index=False),
        file_name="dataset_manifest_filtered.csv",
        mime="text/csv",
    )


def sources_page() -> None:
    st.title("Fontes")

    df = sources_df()

    with st.form("source_form"):
        st.subheader("Cadastro")
        col_left, col_right = st.columns(2)
        source_id = col_left.text_input("ID da fonte")
        source_name = col_right.text_input("Nome")
        homepage_url = col_left.text_input("Homepage")
        license_url = col_right.text_input("Termos/licenca")
        source_type = col_left.text_input("Tipo de fonte")
        access_type = col_right.selectbox(
            "Acesso",
            ["", "public web", "public/research", "controlled access", "internal only"],
        )
        redistribution_status = col_left.selectbox(
            "Redistribuicao",
            ["", "verify before redistribution", "per dataset license", "controlled access", "not an image source"],
        )
        notes = st.text_area("Notas", height=80)

        if st.form_submit_button("Salvar fonte", type="primary"):
            cleaned_source_id = source_id.strip()
            if not cleaned_source_id:
                st.error("Informe o ID da fonte.")
            else:
                new_row = {
                    "source_id": cleaned_source_id,
                    "source_name": source_name.strip(),
                    "homepage_url": homepage_url.strip(),
                    "source_type": source_type.strip(),
                    "access_type": access_type.strip(),
                    "redistribution_status": redistribution_status.strip(),
                    "license_or_terms_url": license_url.strip(),
                    "notes": notes.strip(),
                }
                df = df[df["source_id"] != cleaned_source_id]
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_table(SOURCE_CATALOG, df[SOURCE_COLUMNS])
                st.success("Fonte salva.")
                st.rerun()

    st.subheader("Catalogo")
    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        height=420,
        hide_index=True,
    )

    if st.button("Salvar tabela editada", use_container_width=True):
        save_table(SOURCE_CATALOG, edited)
        st.success("Catalogo salvo.")
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Dermatology Dataset", layout="wide")
    page = sidebar()

    if page == "Painel":
        dashboard_page()
    elif page == "Registrar imagem":
        register_page()
    elif page == "Validacao":
        validation_page()
    elif page == "Manifesto":
        manifest_page()
    elif page == "Fontes":
        sources_page()


if __name__ == "__main__":
    main()
