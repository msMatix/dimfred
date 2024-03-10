import json
import os
from typing import Union

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


################################################################################
# HELPER
################################################################################
class ABI_(list):
    def __init__(self, path_or_list: Union[list, str]):
        if isinstance(path_or_list, str):
            self.path = path_or_list
            self.load()
        else:
            self.path = ""
            self._load_list(path_or_list)

    def load(self):
        self.clear()

        with open(self.path, "r") as f:
            j = json.load(f)

        for v in j["abi"]:
            self.append(v)

    def _load_list(self, l):
        self.clear()
        for i in l:
            self.append(i)


################################################################################
# TYPES
################################################################################
ABI = Union[ABI_, str]


################################################################################
# CONFIG
################################################################################
class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"config_{os.environ['APP_CONFIG']}.env", env_file_encoding="utf-8"
    )

    @model_validator(mode="before")
    def parse_abis(cls, values):
        for k, v in values.items():
            if "_abi" in k or "_ABI" in k:
                values[k] = ABI_(v)

        return values
