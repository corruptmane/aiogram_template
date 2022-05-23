### [![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/) [![aiogram](https://img.shields.io/badge/aiogram-2.20-blue)](https://pypi.org/project/aiogram/)

Scalable and straightforward template for bots written in [aiogram](https://github.com/aiogram/aiogram).

---

### Setting it up

#### System dependencies

- Python 3.10
- Git

#### Preparations

- Clone this repo via HTTPS URL or SSH URL
    - HTTPS `git clone https://github.com/corruptmane/aiogram_template.git`
    - SSH `git clone git@github.com:corruptmane/aiogram_template.git`
- Move to the directory `cd aiogram_template`
- If you want to use webhooks, you can create self-signed SSL certificate by executing `./gen_ssl` shell script. Before executing, run `chmod +x gen_ssl` to allow executing on this script

#### Docker Deployment

- **Note:** You need to have Docker and Docker Compose installed:
    - Arch-based distro: `sudo pacman -S docker docker-compose`
    - Debian-based distro: `sudo apt install docker docker-compose`
- Rename `env.example` to `.env` and replace variables to your own
- Run command: `docker-compose up`

#### Maintenance

- Stop the exist docker-container `docker-compose down`
- Rebuild containers and start bot (if you've edited some part of bot) `docker-compose up`
