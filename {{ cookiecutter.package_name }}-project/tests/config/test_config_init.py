# -*- coding: utf-8 -*-

import os
import pytest
from {{ cookiecutter.package_name }}.config.init import config


def test():
    # constant
    _ = config

    _ = config.env

    # constant attributes

    # derived attributes


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
