# Makefile
.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Editor
vscode: ## open vscode (with virtual environment activated from poetry)
	@sed -i 's#\("python.defaultInterpreterPath":\).*#\1 "'$$(poetry env info --path | awk '!/Activated/{print}')'",#' .vscode/settings.json && code .
	
##@ Formatters

format-black: ## run black (code formatter)
	@black .

format-isort: ## run isort (imports formatter)
	@isort .

format: format-black format-isort ## run all formatters

##@ Linters

lint-black: ## run black in linting mode
	@black . --check

lint-isort: ## run isort in linting mode
	@isort . --check

lint-flake8: ## run flake8 (code linter)
	@flake8 .

lint-mypy: ## run mypy (static-type checker)
	@mypy ./src/app

lint-mypy-report: ## run mypy & create report
	@mypy ./src/app --html-report ./mypy_html

lint-bandit: ## run bandit (security linter)
	@bandit -r ./src/app 

lint-bandit-report: ## run bandit & create report
	@bandit -r ./src/app -f html -o ./bandit_html/index.html

lint: lint-black lint-isort lint-flake8 lint-mypy lint-bandit ## run all linters

##@ Run
run: ## run the application
	@poetry run start
dev: ## run the application in development mode
	@poetry run uvicorn app.app:app --host 0.0.0.0 --reload