FROM python:3.10-slim-buster

WORKDIR /src
ENV PYTHONPATH "${PYTHONPATH}:/src/"

COPY . /src
RUN python -m pip install -U pip && python -m pip install -r requirements.txt
RUN chmod +x /src/docker-entrypoint.sh

ENTRYPOINT ["sh", "/src/docker-entrypoint.sh"]

