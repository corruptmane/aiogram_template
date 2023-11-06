from pathlib import Path
from typing import TypeVar, Type

import yaml

from src.common import dcf_load, get_config_file_path, get_app_dir_path

T = TypeVar("T")


def _read_by_path(path: Path) -> dict:
    with path.open('rb') as f:
        return yaml.safe_load(f)


def _read_by_string(path: str) -> dict:
    with open(path, "rb") as f:
        return yaml.safe_load(f)


def read_file(path: str | Path) -> dict:
    if isinstance(path, Path):
        return _read_by_path(path)
    else:
        return _read_by_string(path)


def load_config(config_type: Type[T], config_scope: str | None = None, path: str | Path | None = None) -> T:
    if path is None:
        path = get_config_file_path(get_app_dir_path())

    data = read_file(path)

    if config_scope is not None:
        data = data[config_scope]

    config = dcf_load(data, config_type)
    return config
