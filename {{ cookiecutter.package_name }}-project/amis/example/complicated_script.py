# -*- coding: utf-8 -*-

print("========== Complicated Script starts here ==========")

from {{ cookiecutter.package_name }} import __version__

print(f"{{ cookiecutter.package_name }} version: {__version__}")

from {{ cookiecutter.package_name }}.config.init import config

print(config)
