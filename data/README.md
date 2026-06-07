# Data Layout

## `raw/`

Guarda arquivos originais por fonte. Para DermNetNZ:

```text
raw/dermnetnz/
  pages/   # HTML ou snapshots de paginas, quando permitido
  images/  # imagens originais, quando permitido
```

## `processed/`

Guarda imagens derivadas e conjuntos de treino/validacao/teste.

```text
processed/
  images/  # imagens redimensionadas, normalizadas ou anonimizadas
  splits/  # CSVs com divisao train/val/test
```

Arquivos grandes nao entram no git por padrao.
