# -*- coding: utf-8 -*-

print("========== Complicated Script starts here ==========")

import {{ cookiecutter.package_name }}

print(f"{{ cookiecutter.package_name }} version: {{{ cookiecutter.package_name }}.__version__}")

from {{ cookiecutter.package_name }}.config.init import config

print(config)
