target install:
	python -m playwright install
	pip install --upgrade uv
	uv venv
	uv sync --frozen
