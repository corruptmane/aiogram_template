[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/downloads/) [![aiogram](https://img.shields.io/badge/aiogram-3.1.1-blue)](https://pypi.org/project/aiogram/)

Scalable and straightforward template for bots written in [aiogram](https://github.com/aiogram/aiogram).

---

### Setting it up

#### System dependencies

- Python 3.11
- Poetry
- Git

#### Preparations

1. Clone this repo via:
    - HTTPS `git clone https://github.com/corruptmane/aiogram_template.git`
    - SSH `git clone git@github.com:corruptmane/aiogram_template.git`
2. Move to the directory `cd aiogram_template`
3. Rename `dist.config.yml` to `config.yml` (or `docker_config.yml` depends on would you deploy by docker or not) and replace variables to your own

#### Regular Deployment

1. Install requirements: `poetry install`
2. Run your bot: `poetry run tgbot`

#### Docker Deployment

1. Deploy your infrastructure (Redis, PostgreSQL, etc.). Example `infra.docker-compose.yml` file is in `deploy` directory
2. Build docker image: `docker build -f deploy/Dockerfile -t template_bot:latest .`
3. Run command: `docker-compose up -d`