# datasetdermato

Estrutura inicial para organizar um dataset de imagens dermatologicas com foco em rastreabilidade, metadados padronizados proprios e separacao clara entre imagens, casos, anotacoes e fontes.

## Objetivo

Este repositorio organiza imagens dermatologicas coletadas de fontes publicas ou autorizadas, como paginas educacionais do DermNetNZ, datasets listados em revisoes publicas e colecoes institucionais. A estrutura foi pensada para pesquisa, curadoria e preparacao de dados para modelos de classificacao ou segmentacao.

## Estrutura

```text
datasetdermato/
  data/
    raw/                 # arquivos originais por fonte
    processed/           # imagens normalizadas e splits
  metadata/
    standardized/        # metadados centrais do projeto, inspirados por padroes externos
    relational/          # tabelas CSV equivalentes ao modelo relacional
    sources/             # catalogo e manifesto de coleta por fonte
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
- `database/schema.sql`: schema PostgreSQL para o modelo institucional.
- `metadata/sources/source_catalog.csv`: cadastro das fontes e status de permissao.
- `metadata/sources/candidate_datasets.csv`: datasets dermatologicos candidatos para revisao.
- `metadata/sources/dermnetnz_manifest.csv`: manifesto de paginas/imagens do DermNetNZ.
- `annotations/labels/taxonomy.csv`: taxonomia inicial para doencas e grupos clinicos.
- `docs/collection_protocol.md`: fluxo recomendado de coleta e curadoria.
- `docs/santa_casa_strategy.md`: estrategia para acervo institucional com patologia desde 1998.
- `docs/data_dictionary.md`: dicionario de campos especificos do projeto.
- `docs/annotation_protocol.md`: protocolo de anotacao de lesoes.
- `docs/ethics_protocol.md`: governanca etica, LGPD, CEP e acesso.
- `docs/dermnetnz_curation.md`: guia especifico para curadoria DermNetNZ.
- `docs/licensing_and_ethics.md`: cuidados com licenca, privacidade e redistribuicao.

## Regras praticas

1. Nao versionar imagens brutas no git sem decisao explicita de licenca e tamanho.
2. Registrar toda imagem no manifesto da fonte antes de mover para `processed`.
3. Preservar URL, atribuicao, licenca, data de acesso e status de permissao.
4. Usar identificadores internos estaveis para paciente, lesao e imagem.
5. Separar diagnostico original, diagnostico normalizado e diagnostico revisado.

## Referencias usadas

- ISIC metadata template, data dictionary 2.4 e wiki de imagem usados como inspiracao, nao como modelo obrigatorio.
- ISIC Archive image metadata wiki: https://github.com/ImageMarkup/isic-archive/wiki/Image#metadata
- DermNetNZ: https://dermnetnz.org/
- Skinive review de datasets: https://skinive.com/skin-disease-datasets/

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
