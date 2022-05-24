[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/) [![aiogram](https://img.shields.io/badge/aiogram-2.20-blue)](https://pypi.org/project/aiogram/)

Scalable and straightforward template for bots written in [aiogram](https://github.com/aiogram/aiogram).

---

### Setting it up

#### System dependencies

- Python 3.10
- Git

#### Preparations

1. Clone this repo via:
    - HTTPS `git clone https://github.com/corruptmane/aiogram_template.git`
    - SSH `git clone git@github.com:corruptmane/aiogram_template.git`
2. Move to the directory `cd aiogram_template`
3. If you want to use webhooks, you can create self-signed SSL certificate by executing `./gen_ssl` shell script. Before executing, run `chmod +x gen_ssl` to allow executing on this script
4. Rename `env.example` to `.env` and replace variables to your own

#### Regular Deployment

1. Create a virtual environment: `python -m venv venv`
2. Activate a virtual environment:
    - You use sh or zsh: `source ./venv/bin/activate` or `. ./venv/bin/activate`
    - You use fish: `source ./venv/bin/activate.fish` or `. ./venv/bin/activate.fish`
    - You use csh: `source ./venv/bin/activate.csh` or `. ./venv/bin/activate.csh`
3. Install requirements: `pip install -r requirements.txt`
4. Run your bot: `python -O bot.py`

#### Docker Deployment

1. **Note:** You need to have Docker and Docker Compose installed:
    - Arch-based distro: `sudo pacman -S docker docker-compose`
    - Debian-based distro: `sudo apt install docker docker-compose`
2. Run command: `docker-compose up`

#### Maintenance

- Stop the exist docker-container `docker-compose down -v --remove-orphans --rmi local`
- Rebuild containers and start bot (if you've edited some part of bot) `docker-compose up --build`
