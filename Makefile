default: help

dev-setup:
	@python3 -m venv .virtualenv/
	@. .virtualenv/bin/activate
	@pip install -r requirements/prod.in
	@pip install -e .

start-fixtures:
	cd docker && docker compose up

stop-fixtures:
	cd docker && docker compose down --volumes

check-code:
	@.virtualenv/bin/flake8 --ignore=W191,E501 src/
	# @.virtualenv/bin/mypy src/

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rfv ./src/*egg-info

run-web:
	@fastapi dev src/myapp/web/app.py

run-tests:
	export PYTHONDONTWRITEBYTECODE=1
	@.virtualenv/bin/pytest

help:
	@echo 'help'
