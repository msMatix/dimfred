import os

import pytest

from dimfred import BaseConfig


def test_okay_config():
    os.environ["a"] = "1"
    os.environ["b"] = "2"

    c = BaseConfig("tests/test_config.yaml")

    assert c.n0 == "1 2"
    assert c.n1.n2 == "1 2"
    assert c.n1.n3[0] == "1"
    assert c.n1.n3[1] == "2"

