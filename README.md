[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/) [![aiogram](https://img.shields.io/badge/aiogram-2.22.1-blue)](https://pypi.org/project/aiogram/)

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
    - You use sh or bash or zsh: `source ./venv/bin/activate` or `. ./venv/bin/activate`
    - You use fish: `source ./venv/bin/activate.fish` or `. ./venv/bin/activate.fish`
    - You use csh: `source ./venv/bin/activate.csh` or `. ./venv/bin/activate.csh`
3. Install requirements: `pip install -r requirements.txt`
4. Run your bot: `python -O bot.py`

#### Docker Deployment

1. **Note:** You need to have Docker and Docker Compose installed:
    - Arch-based distro: `sudo pacman -S docker docker-compose`
    - Debian-based distro: `sudo apt install docker docker-compose`
2. Run command: `docker-compose up -d`

#### CI/CD

1. You need to add some secrets in your GitHub repository settings, such as:
    - Docker Hub:
        1. `DOCKER_LOGIN` - Login of your Docker Hub account
        2. `DOCKER_PASSWORD` - Password of your Docker Hub account
    - Server (SSH Credentials):
        1. `SERVER_HOST` - IP/URL of server to which you want to deploy your bot
        2. `SERVER_PORT` - Port opened for SSH connections on target server
        3. `SERVER_USER` - User to which we are connecting (such as `root` or `ubuntu`)
        4. `SERVER_KEY` - SSH Private Key used to authenticate to target server (string)
2. Correctly set up your .env variable named `BOT_IMAGE_NAME` to something like this:
`BOT_IMAGE_NAME=your_docker_login/repository_name:latest`
3. On your server you need to have only `docker-compose.yml` and `.env` files to successfully run your project
4. Test CI/CD runs manually in Actions section of repository.
After successful tests, you can edit `.github/workflows/cicd.yml` file to set up triggers when this pipeline would be triggered (e.g. push to master branch)

