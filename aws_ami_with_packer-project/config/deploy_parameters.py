# -*- coding: utf-8 -*-

from aws_ami_with_packer import __version__
from aws_ami_with_packer.boto_ses import bsm
from aws_ami_with_packer.config.init import config

tags = {
    "tech:project_name": config.project_name,
    "tech:env_name": config.env.env_name,
    "tech:version": __version__,
    "tech:human_creator": "Firstname Lastname",
    "tech:machine_creator": "packer",
    "auto:delete_at": "na",
    "bus:ou": "app",
    "bus:team": "app",
    "bus:project": "poc",
    "bus:owner": "Firstname Lastname",
}

config.deploy(bsm=bsm, parameter_with_encryption=True, tags=tags)
# config.delete(bsm=bsm, use_parameter_store=True)