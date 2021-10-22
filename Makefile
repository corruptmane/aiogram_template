include .env

PYTHONPATH := ${PYTHONPATH}:${shell pwd}/app/

default:help

help:
	@echo "USAGE"
	@echo " make <command> [args]"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo " migrate			Run migration"
	@echo " migration name=<name>\t\tCreate migration with name <message>"
	@echo " downgrade			Run downgrade to -1 migration"
	@echo " build				(Re)build your containers and (re)create services"
	@echo " start				Start your bot in containers (use only if containers and services created)"
	@echo " restart				Restart your bot (if you don't need to rebuild)"
	@echo " run					Run your bot (if you don't need to rebuild)"
	@echo " stop				Stop your bot, removing containers and networks"
	@echo " black				Run black"
	@echo " isort				Run isort"
	@echo " lint				Run black and isort"

migrate:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic upgrade head

migration:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic revision --autogenerate -m "${name}"

downgrade:
	PYTHONPATH=${shell pwd}:${PYTHONPATH} alembic downgrade -1

build:
	sudo docker compose build && sudo docker compose create

start:
	sudo docker compose start

restart:
	sudo docker compose restart

run:
	sudo docker compose up

stop:
	sudo docker compose down

black:
	python -m black . --exclude \[pgdata\|redis\]

isort:
	python -m isort . --skip pgdata --skip redis

lint: black isort
