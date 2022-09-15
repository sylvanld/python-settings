VENV=.venv
BIN=$(VENV)/bin

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

$(VENV):
	virtualenv -p python3 .venv

install: $(VENV) ## Install development dependencies
	$(BIN)/pip install -r requirements/dev.txt	

format: ## Format code according to best practices
	$(BIN)/black .
	$(BIN)/isort .

test: ## Run unittests using pytest
	$(BIN)/python -m pytest tests/

main: ## Run main entrypoint
	$(BIN)/python main.py

