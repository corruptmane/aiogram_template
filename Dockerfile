FROM python:3.10-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/src"

WORKDIR /src

COPY . /src

RUN python -m pip install --upgrade pip && python -m pip install --requirement requirements.txt

ENTRYPOINT python -m alembic upgrade head && python -O bot.py
