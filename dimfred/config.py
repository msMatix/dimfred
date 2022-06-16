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
        splitted = match.split(":")
        # no extension just try with default empty
        if len(match) == 1:
            operator = lambda: os.environ.get(splitted[0], "")
        # env var has to be set
        elif splitted[1] == "!":
            operator = lambda: os.environ[splitted[0]]
        # default value
        else:
            operator = lambda: os.environ.get(splitted[0], splitted[1])

        s = s.replace(f"${{{match}}}", operator())

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
