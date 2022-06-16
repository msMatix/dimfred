import os
from pathlib import Path

import pytest

from dimfred import BaseConfig


def test_okay_config():
    os.environ["a"] = "1"
    os.environ["b"] = "2"
    os.environ["MUST"] = "MUST"

    c = BaseConfig("tests/test_config.yaml")

    assert c.n0 == "1 2"
    assert c.n1.n2 == "1 2"
    assert c.n1.n3[0] == "1"
    assert c.n1.n3[1] == "2"
    assert isinstance(c.n4, Path)
    assert c.n6 == "default"

def test_fail_if_not_set():
    del os.environ["MUST"]

    with pytest.raises(Exception):
        c = BaseConfig("tests/test_config.yaml")


