# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }} import __version__
from {{ cookiecutter.package_name }}.boto_ses import bsm
from {{ cookiecutter.package_name }}.config.init import config

tags = {
    "tech:project_name": config.project_name,
    "tech:env_name": config.env.env_name,
    "tech:version": __version__,
    "tech:human_creator": "{{ cookiecutter.author_name }}",
    "tech:machine_creator": "packer",
    "auto:delete_at": "na",
    "bus:ou": "app",
    "bus:team": "app",
    "bus:project": "poc",
    "bus:owner": "{{ cookiecutter.author_name }}",
}

config.deploy(bsm=bsm, parameter_with_encryption=True, tags=tags)
# config.delete(bsm=bsm, use_parameter_store=True)