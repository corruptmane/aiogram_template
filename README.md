### [![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue)](https://www.python.org/downloads/) [![aiogram](https://img.shields.io/badge/aiogram-2.15-blue)](https://pypi.org/project/aiogram/)

Scalable and straightforward template for bots written in [aiogram](https://github.com/aiogram/aiogram).

---

### Setting it up

#### System dependencies

- Python 3.7+
- GNU/Make
- Git

#### Preparations

- Clone this repo via HTTPS URL or SSH URL;
    - HTTP `git clone https://github.com/vyr0d0k/aiogram_template.git`
    - SSH `git clone git@github.com:vyr0d0k/aiogram_template.git`
- Move to the directory `cd aiogram_template`.

#### Docker Deployment

- **Note:** You need to have Docker installed:
    - Arch Linux package manager: `sudo pacman -S docker`
- Rename `.env.dist` to `.env` and replace variables to your own
- Run command: `sudo docker compose up`

#### Maintenance

*Use `make help` to view all available commands*

- Reformat the code `make lint`
- Stop the exist docker-container `make stop`
- Rebuild containers and start bot (if you've edited some part of bot) `make build start`
- Create new migration with name \<name\>(if you've edited some database tables) `make migration name=<name>`
- Upgrade database after creating new migration `make migrate`
