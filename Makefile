include .env

PYTHONPATH := ${PYTHONPATH}:${shell pwd}/tgbot/

default:help

help:
	@echo "USAGE:"
	@echo "	make <command>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "	migrate			Run migrations"
	@echo "	migration name=<name>	Autogenerate migration with name <name>"
	@echo "	downgrade		Run downgrade to -1 migration"
	@echo "	black			Run black"
	@echo "	isort			Run isort"
	@echo "	lint			Run black and isort"

migrate:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic upgrade head

migration:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic revision --autogenerate -m "${name}"

downgrade:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic downgrade -1

black:
	python -m black . --exclude \[pgdata\|redisdata\]

isort:
	python -m isort . --skip pgdata --skip redisdata

lint: black isort
