PYTHON ?= python3

.PHONY: install validate test app stats

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

validate:
	$(PYTHON) scripts/dataset_validate.py

app:
	$(PYTHON) -m streamlit run scripts/dataset_app.py

stats:
	$(PYTHON) scripts/dataset_stats.py --csv
