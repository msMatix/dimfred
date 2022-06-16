import os
import re
from pathlib import Path
from typing import Union

from easydict import EasyDict as edict


def _load_vars(config, replace_vars):
    for k, v in config.items():
        if isinstance(v, str):
            config[k] = replace_vars(v)
        elif isinstance(v, (dict, edict)):
            config[k] = _load_vars(v, replace_vars)
        elif isinstance(v, list):
            config[k] = [replace_vars(v_) if isinstance(v_, str) else v_ for v_ in v]

    return config


def _replace_env_vars(s):
    r = "\\${([^}]*)}"
    matches = re.findall(r, s)

    for match in matches:
        s = s.replace(f"${{{match}}}", os.environ.get(match, ""))

    return s


def _replace_path_vars(s):
    r = "P{([^}]*)}"
    matches = re.findall(r, s)
    for match in matches:
        s = Path(match)

    return s


class BaseConfig:
    def __init__(self, path: Union[str, Path], config: dict = {}):
        if path:
            path = str(path)
            if path.endswith("yaml"):
                import yaml

                load = yaml.safe_load
            elif path.endswith("json"):
                import json

                load = json.load
            elif path.endswith("jsonc"):
                from jsoncomment import JsonC

                load = JsonC().load
            else:
                raise Exception(f"Unknown filetype: {path}")

            with open(path, "r") as f:
                config = load(f)

            config = edict(config)
            config = _load_vars(config, _replace_env_vars)
            config = _load_vars(config, _replace_path_vars)

        for k, v in config.items():
            setattr(self, k, v)
