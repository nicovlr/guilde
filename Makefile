.PHONY: setup test run-server lint generate-data clean help

PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin

help:
	@echo "Targets: setup | test | lint | run-server | generate-data | clean"

setup: $(VENV)/bin/activate
	$(BIN)/pip install -e "./ai-server[dev]" -e "./data[dev]"
	@echo "Setup OK. Copy .env.example → .env if needed."

$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip

lint:
	$(BIN)/ruff check ai-server/src ai-server/tests data/src data/tests
	$(BIN)/ruff format --check ai-server/src ai-server/tests data/src data/tests

test:
	$(BIN)/pytest ai-server/tests data/tests -q

run-server:
	LLM_MODE=$${LLM_MODE:-mock} $(BIN)/uvicorn guilde_ai.main:app --host $${AI_SERVER_HOST:-127.0.0.1} --port $${AI_SERVER_PORT:-8000} --reload

generate-data:
	$(BIN)/python -m guilde_data.cli --seed $${COMPANY_SEED:-42} --out data/output/company.json

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
