import os
from dataclasses import dataclass
from pathlib import Path


def get_app_dir_path() -> Path:
    if path := os.getenv('APP_DIR'):
        return Path(path)

    app_dir = Path(__file__)
    while not (app_dir / 'src').exists():
        app_dir = app_dir.parent
        continue
    return app_dir


def get_config_file_path(app_dir: Path) -> Path:
    config_file_name = os.getenv('CONFIG_FILE_NAME', 'config.yml')
    return app_dir / 'config' / config_file_name


@dataclass(frozen=True, slots=True, kw_only=True)
class Paths:
    app_dir: Path

    @property
    def config_file_path(self) -> Path:
        return get_config_file_path(self.app_dir)

    @property
    def data_dir_path(self) -> Path:
        return self.app_dir / 'data'
