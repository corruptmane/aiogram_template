include .env

PYTHONPATH := ${PYTHONPATH}:${shell pwd}/app/

default:help

help:
	@echo "USAGE"
	@echo " make <command> [args]"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo " migrate			Run migration"
	@echo " black				Run black"
	@echo " isort				Run isort"
	@echo " lint				Run black and isort"

migrate:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic upgrade head

migration:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic revision --autogenerate -m "${message}"

downgrade:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic downgrade -1

black:
	python -m black .

isort:
	python -m isort .

lint: black isort
