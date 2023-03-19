# -*- coding: utf-8 -*-

print("========== Complicated Script starts here ==========")

from aws_ami_with_packer import __version__

print(f"aws_ami_with_packer version: {__version__}")

from aws_ami_with_packer.config.init import config

print(config)
