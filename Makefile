PYTHON ?= python3

.PHONY: install validate app

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

validate:
	$(PYTHON) scripts/dataset_validate.py

app:
	$(PYTHON) -m streamlit run scripts/dataset_app.py
