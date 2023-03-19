# -*- coding: utf-8 -*-

import os
import pytest
import aws_ami_with_packer


def test_import():
    _ = aws_ami_with_packer


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
