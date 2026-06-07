---
license: cc-by-4.0
task_categories:
  - image-classification
  - object-detection
language:
  - pt
  - en
tags:
  - dermatology
  - medical-imaging
  - skin-lesion
  - dermoscopy
  - histopathology
  - clinical-images
  - LGPD
  - Brazil
pretty_name: Dermatology Service Dataset
size_categories:
  - n<1K
---

# dermatology-service-dataset

[![Dataset validation](https://github.com/hampikamayuq/datasetdermato/actions/workflows/validate.yml/badge.svg)](https://github.com/hampikamayuq/datasetdermato/actions/workflows/validate.yml)

Repositorio profissional para organizar, anonimizar, curar, auditar e disponibilizar de forma controlada datasets dermatologicos retrospectivos de servicos universitarios, hospitalares ou academicos.

O projeto foi desenhado para acervos acumulados ao longo de anos ou decadas de assistencia, ensino e pesquisa, contendo imagens clinicas, dermatoscopicas, cirurgicas e histopatologicas, com metadados clinicos, laudos, revisao por especialistas, governanca etica e trilhas de auditoria.

## Para Quem

Este repositorio pode ser adaptado por:

- servicos de dermatologia
- hospitais universitarios
- departamentos academicos
- centros de referencia
- ambulatorios especializados
- laboratorios de dermatopatologia
- grupos de pesquisa em IA medica e dermatologia

O projeto e independente de qualquer instituicao especifica.

## Escopo Clinico

O dataset foi pensado para multiplas subespecialidades:

- dermatologia clinica
- dermatopediatria
- cirurgia dermatologica
- oncologia cutanea
- dermatopatologia
- dermatoscopia
- doencas inflamatorias
- doencas autoimunes
- tricologia
- hansenologia
- dermatologia tropical
- dermatologia infecciosa
- ambulatorio de lesoes pigmentadas
- ambulatorio de tumores cutaneos

## Cadeia de Dados

O modelo permite vincular um caso dermatologico completo:

```text
imagem clinica
  -> dermatoscopia
  -> procedimento cirurgico
  -> laudo histopatologico
  -> revisao por especialistas
  -> seguimento clinico
```

Essa cadeia e mais valiosa cientificamente do que uma colecao de imagens soltas, porque permite separar diagnostico assistencial, revisao especializada e confirmacao histopatologica.

## Niveis de Evidencia

O projeto usa tres niveis:

- `bronze`: imagem clinica + diagnostico assistencial original
- `silver`: imagem clinica + revisao por especialista
- `gold`: imagem clinica + histopatologia + revisao especializada

A divisao `train` / `validation` / `test` deve ser feita por paciente, nunca apenas por imagem.

## Origem e Subespecialidade

Cada caso pode registrar:

- `source_type`: origem do caso ou acervo
- `specialty_service`: subespecialidade ou linha assistencial

Valores previstos para `source_type`:

- `faculty_collection`
- `resident_collection`
- `pathology_archive`
- `clinical_archive`
- `conference_archive`
- `research_project`
- `private_practice_archive`
- `institutional_database`

Valores previstos para `specialty_service`:

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

Esses campos permitem auditar desempenho, vies e qualidade por origem dos dados e por subespecialidade.

## Estrutura

```text
dermatology-service-dataset/
  data/
    raw/                 # arquivos originais por fonte
    anonymized/          # imagens anonimizadas
    processed/           # imagens normalizadas e splits
  metadata/
    standardized/        # metadados centrais por imagem
    relational/          # tabelas CSV equivalentes ao modelo relacional
    sources/             # catalogo de fontes e manifestos de coleta
    audits/              # auditoria de qualidade, duplicatas, leakage e fairness
  database/              # schema PostgreSQL
  annotations/
    labels/              # taxonomia e mapeamentos
    masks/               # mascaras de segmentacao, quando existirem
  docs/                  # protocolos, governanca e documentacao cientifica
  notebooks/             # exploracao e analise
  references/            # arquivos de referencia externos
  scripts/               # validacao e preparacao de metadados
```

## Arquivos Principais

Metadados:

- `metadata/dataset_manifest.csv`: manifesto central por imagem.
- `metadata/standardized/core_metadata_template.csv`: template padronizado por imagem.
- `metadata/standardized/core_metadata_schema.json`: schema de validacao dos campos centrais.
- `metadata/relational/*.csv`: tabelas para pacientes, casos, imagens, patologia, procedimentos, revisoes, anotacoes, etica e splits.
- `metadata/audits/quality_audit.csv`: auditoria de duplicatas, leakage, rotulos, qualidade e identificadores.
- `metadata/audits/fairness_summary_template.csv`: sumario de representatividade por subgrupo.

Banco de dados:

- `database/schema.sql`: schema PostgreSQL relacional.

Documentacao:

- `docs/service_dataset_strategy.md`: estrategia para acervos institucionais retrospectivos.
- `docs/quickstart.md`: caminho curto para validar e registrar imagens.
- `docs/data_dictionary.md`: dicionario de dados.
- `docs/datasheet_for_dataset.md`: datasheet do dataset.
- `docs/dataset_card.md`: dataset card.
- `docs/quality_audit_protocol.md`: protocolo de auditoria.
- `docs/fairness_bias_plan.md`: plano de vies e representatividade.
- `docs/publication_guidelines.md`: TRIPOD+AI, STARD-AI e CONSORT-AI.
- `docs/ethics_protocol.md`: LGPD, CEP/CONEP e governanca.
- `docs/literature_review.md`: referencias cientificas e decisoes aplicadas.
- `docs/annotation_protocol.md`: bbox, mascara, poligono e regioes de exclusao.
- `docs/collection_protocol.md`: fluxo de coleta e curadoria.
- `docs/licensing_and_ethics.md`: licenca, privacidade e redistribuicao.

Scripts:

- `scripts/register_image.py`: registra uma imagem (remove EXIF, detecta duplicata, escreve nos manifestos).
- `scripts/dataset_app.py`: abre a ferramenta visual de curadoria com registro, validacao, manifesto e fontes.
- `scripts/dataset_validate.py`: validador Python portavel para metadados, fontes e tabelas relacionais.
- `scripts/dataset_constants.py`: constantes compartilhadas do dataset.
- `scripts/dataset_ops.py`: modulo compartilhado usado pelo CLI e pela UI.
- `scripts/ui_register.py`: interface visual Streamlit mantida como entrada compativel.
- `scripts/validate_metadata.ps1`
- `scripts/validate_sources.ps1`
- `scripts/validate_relational_metadata.ps1`
- `scripts/validate_all.ps1`
- `scripts/validate_all.sh`
- `scripts/run_app.ps1`
- `scripts/run_app.sh`
- `scripts/new_split_template.ps1`
- `scripts/ingest_image.py`: modulo de utilidades usado pelo register_image.
- `Makefile`: atalhos `make install`, `make validate` e `make app` para macOS/Linux.

## Regras Praticas

1. Nao versionar imagens brutas no Git sem decisao explicita de licenca, governanca e tamanho.
2. Registrar toda imagem em manifesto antes de processar.
3. Preservar origem, URL, atribuicao, licenca, data de acesso e status etico.
4. Usar identificadores internos estaveis e hashes para paciente, caso, lesao, imagem e laudo.
5. Separar diagnostico original, diagnostico normalizado, diagnostico revisado e diagnostico histopatologico.
6. Registrar `source_type` e `specialty_service` para auditoria cientifica.
7. Auditar duplicatas, near-duplicates, leakage entre splits, rotulos e identificadores antes de qualquer release.
8. Reportar representatividade por fototipo/skin tone, idade, sexo, topografia, origem e subespecialidade quando eticamente permitido.

## Instalar

macOS/Linux:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Validacao

Com Python, em qualquer sistema:

```bash
python scripts/dataset_validate.py
```

macOS/Linux tambem podem usar:

```bash
sh scripts/validate_all.sh
make validate
```

No Windows, ha um atalho PowerShell com fallback para os validadores antigos:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_all.ps1
```

## Testes no GitHub

O reposititorio usa GitHub Actions em `.github/workflows/validate.yml` para testar Linux, macOS e Windows.

O workflow roda automaticamente em `push` e `pull_request`. Tambem pode ser executado manualmente em:

```text
GitHub -> Actions -> Dataset validation -> Run workflow
```

## Ferramenta Visual

macOS/Linux:

```bash
sh scripts/run_app.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_app.ps1
```

Com Python, em qualquer sistema:

```bash
python -m streamlit run scripts/dataset_app.py
```

## Governanca

O projeto deve ser usado com:

- anonimizacao forte
- controle de acesso
- rastreabilidade de origem
- versionamento de releases
- auditoria de qualidade
- documentacao de uso permitido e uso proibido
- revisao etica para dados sensiveis
- compartilhamento controlado para pesquisa cientifica

Para o contexto brasileiro, a arquitetura considera LGPD, avaliacao CEP/CONEP, CNS 466/2012 e CNS 738/2024.

## Referencias

### Dermatologia, Datasets e IA

- Esteva A, Kuprel B, Novoa RA, et al. Dermatologist-level classification of skin cancer with deep neural networks. Nature. 2017. https://www.nature.com/articles/nature21056
- Tschandl P, Rosendahl C, Kittler H. The HAM10000 dataset: A large collection of multi-source dermatoscopic images of common pigmented skin lesions. Scientific Data. 2018. https://www.nature.com/articles/sdata2018161
- ISIC Archive. International Skin Imaging Collaboration. https://www.isic-archive.com/
- ISIC Archive image metadata wiki. https://github.com/ImageMarkup/isic-archive/wiki/Image#metadata
- Daneshjou R, Vodrahalli K, Novoa RA, et al. Disparities in dermatology AI performance on a diverse, curated clinical image set. Science Advances. 2022. https://www.science.org/doi/10.1126/sciadv.abq6147
- DDI: Diverse Dermatology Images dataset. Stanford AIMI. https://aimi.stanford.edu/datasets/ddi-diverse-dermatology-images
- Groh M, Harris C, Soenksen LR, et al. Evaluating deep neural networks trained on clinical images in dermatology with the Fitzpatrick 17k dataset. CVPR Workshops. 2021. https://openaccess.thecvf.com/content/CVPR2021W/ISIC/html/Groh_Evaluating_Deep_Neural_Networks_Trained_on_Clinical_Images_in_Dermatology_CVPRW_2021_paper.html
- Fitzpatrick17k dataset. https://github.com/mattgroh/fitzpatrick17k

### Documentacao, Qualidade e Vies

- Gebru T, Morgenstern J, Vecchione B, et al. Datasheets for Datasets. Communications of the ACM. 2021. https://cacm.acm.org/research/datasheets-for-datasets/
- Skinive review of skin disease datasets. https://skinive.com/skin-disease-datasets/

### Diretrizes de IA Medica

- TRIPOD+AI statement. BMJ. 2024. https://www.bmj.com/content/385/bmj-2023-078378
- CONSORT-AI extension. Nature Medicine. 2020. https://www.nature.com/articles/s41591-020-1034-x
- STARD-AI. Nature Medicine. 2025. https://www.nature.com/articles/s41591-025-03953-8

### Brasil, Etica e Banco de Dados

- Resolucao CNS 466/2012. https://www.gov.br/conselho-nacional-de-saude/pt-br/acesso-a-informacao/atos-normativos/resolucoes/2012/resolucao-no-466.pdf/view
- Resolucao CNS 738/2024. https://www.gov.br/conselho-nacional-de-saude/pt-br/atos-normativos/resolucoes/2024/resolucao-no-738.pdf
- CEP Fiocruz: orientacoes para uso de bases de dados. https://www.cep.epsjv.fiocruz.br/orientacoes-protocolos/uso-de-base-de-dados

## Aviso

Este repositorio organiza dados e metadados para pesquisa. Ele nao e um dispositivo medico, nao valida modelos para uso clinico e nao substitui avaliacao profissional dermatologica.
