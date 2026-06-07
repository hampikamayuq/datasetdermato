# dermatology-service-dataset

Repositorio Git profissional destinado a organizacao, anonimizacao, curadoria, auditoria e disponibilizacao controlada de um dataset dermatologico retrospectivo proveniente de um servico dermatologico universitario/hospitalar.

## Objetivo

O projeto organiza imagens clinicas, dermatoscopicas, cirurgicas e histopatologicas acumuladas ao longo de decadas de assistencia, ensino e pesquisa. Ele foi desenhado para ser independente de qualquer instituicao especifica, permitindo uso por servicos dermatologicos, hospitais universitarios, departamentos academicos, centros de referencia, ambulatorios especializados e grupos de pesquisa em dermatologia.

O dataset suporta multiplas subespecialidades dermatologicas, incluindo dermatologia clinica, dermatopediatria, cirurgia dermatologica, oncologia cutanea, dermatopatologia, dermatoscopia, doencas inflamatorias, doencas autoimunes, tricologia, hansenologia, dermatologia tropical, dermatologia infecciosa, ambulatorio de lesoes pigmentadas e ambulatorio de tumores cutaneos.

O modelo permite vincular:

```text
imagem clinica
  -> dermatoscopia
  -> procedimento cirurgico
  -> laudo histopatologico
  -> revisao por especialistas
  -> seguimento clinico
```

Ele tambem foi preparado para datasets retrospectivos iniciados a partir da decada de 1990 ou anteriores, com potencial integracao de acervos provenientes de professores, assistentes, laboratorios de dermatopatologia, arquivos historicos, apresentacoes cientificas e sistemas institucionais.

## Estrutura

```text
dermatology-service-dataset/
  data/
    raw/                 # arquivos originais por fonte
    processed/           # imagens normalizadas e splits
  metadata/
    standardized/        # metadados centrais do projeto, inspirados por padroes externos
    relational/          # tabelas CSV equivalentes ao modelo relacional
    sources/             # catalogo e manifesto de coleta por fonte
    audits/              # auditoria de qualidade, duplicatas, leakage e fairness
  database/              # schema PostgreSQL
  annotations/
    labels/              # rotulos revisados, taxonomia e mapeamentos
    masks/               # mascaras de segmentacao, quando existirem
  docs/                  # governanca, licencas e protocolo de coleta
  notebooks/             # exploracao e analise
  references/            # arquivos de referencia externos
  scripts/               # validacao e preparacao de metadados
```

## Primeiros arquivos

- `metadata/standardized/core_metadata_template.csv`: colunas centrais do projeto para metadados por imagem.
- `metadata/standardized/core_metadata_schema.json`: schema simples para validar campos principais.
- `metadata/dataset_manifest.csv`: manifesto central com imagem, fonte, hash, label, qualidade e split.
- `metadata/relational/*.csv`: tabelas para pacientes, casos, imagens, patologia, revisoes, anotacoes e splits.
- `metadata/audits/quality_audit.csv`: template para auditoria de duplicatas, leakage, rotulos e qualidade.
- `metadata/audits/fairness_summary_template.csv`: template para sumario de representatividade por subgrupo.
- `database/schema.sql`: schema PostgreSQL para o modelo institucional.
- `metadata/sources/source_catalog.csv`: cadastro das fontes e status de permissao.
- `metadata/sources/candidate_datasets.csv`: datasets dermatologicos candidatos para revisao.
- `metadata/sources/dermnetnz_manifest.csv`: manifesto de paginas/imagens do DermNetNZ.
- `annotations/labels/taxonomy.csv`: taxonomia inicial para doencas e grupos clinicos.
- `docs/collection_protocol.md`: fluxo recomendado de coleta e curadoria.
- `docs/service_dataset_strategy.md`: estrategia para acervos dermatologicos institucionais retrospectivos.
- `docs/data_dictionary.md`: dicionario de campos especificos do projeto.
- `docs/annotation_protocol.md`: protocolo de anotacao de lesoes.
- `docs/ethics_protocol.md`: governanca etica, LGPD, CEP e acesso.
- `docs/datasheet_for_dataset.md`: template de datasheet para documentacao formal do dataset.
- `docs/quality_audit_protocol.md`: protocolo de duplicatas, vazamento, rotulos e qualidade.
- `docs/fairness_bias_plan.md`: plano de representatividade e avaliacao por subgrupos.
- `docs/publication_guidelines.md`: checklist para TRIPOD+AI, STARD-AI e CONSORT-AI.
- `docs/literature_review.md`: referencias cientificas e decisoes de desenho aplicadas.
- `docs/dermnetnz_curation.md`: guia especifico para curadoria DermNetNZ.
- `docs/licensing_and_ethics.md`: cuidados com licenca, privacidade e redistribuicao.

## Regras praticas

1. Nao versionar imagens brutas no git sem decisao explicita de licenca e tamanho.
2. Registrar toda imagem no manifesto da fonte antes de mover para `processed`.
3. Preservar URL, atribuicao, licenca, data de acesso e status de permissao.
4. Usar identificadores internos estaveis para paciente, lesao e imagem.
5. Separar diagnostico original, diagnostico normalizado e diagnostico revisado.
6. Registrar `source_type` e `specialty_service` para auditoria por origem e subespecialidade.
7. Auditar duplicatas, leakage entre splits, qualidade, rotulos e identificadores antes de qualquer release.

## Referencias usadas

- ISIC metadata template, data dictionary 2.4 e wiki de imagem usados como inspiracao, nao como modelo obrigatorio.
- ISIC Archive image metadata wiki: https://github.com/ImageMarkup/isic-archive/wiki/Image#metadata
- DermNetNZ: https://dermnetnz.org/
- Skinive review de datasets: https://skinive.com/skin-disease-datasets/
- Esteva et al. 2017; HAM10000; DDI; Fitzpatrick17k; DERM12345; Datasheets for Datasets; TRIPOD+AI; CONSORT-AI; STARD-AI; CNS 466/2012; CNS 738/2024.

## Validacao

No PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate_metadata.ps1
powershell -ExecutionPolicy Bypass -File scripts/validate_sources.ps1
powershell -ExecutionPolicy Bypass -File scripts/validate_relational_metadata.ps1
```

## Modelo cientifico

O projeto usa niveis de evidencia:

- `bronze`: imagem clinica + diagnostico assistencial original
- `silver`: imagem clinica + revisao por especialista
- `gold`: imagem clinica + histopatologia + revisao especializada

A divisao `train`/`validation`/`test` deve ser feita por paciente, nunca apenas por imagem.

## Governanca

Toda a arquitetura deve ser compativel com LGPD, anonimizacao forte, governanca de dados sensiveis, rastreabilidade, versionamento e compartilhamento controlado para pesquisa cientifica.
