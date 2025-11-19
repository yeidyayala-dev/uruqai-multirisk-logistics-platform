setup:
	conda env create -f environment.yml

test:
	pytest -q

lint:
	ruff check src/ --fix
	black --check src/
	mypy src/

validate:
	python -m src.common.validation

dash:
	streamlit run dashboards/streamlit_app/app.py

bench:
	python benchmarking/run_benchmarks.py
