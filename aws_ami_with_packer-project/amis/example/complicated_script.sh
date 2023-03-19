#!/bin/bash
#
# This is an example script to run arbitrary complicated provisioning logics
# in Python. Basically, you can put your provisioning logics in a Python library
# (not just a script, but a library that split logics into modules and import
# each other). Then you can use this script to:
#
# 1. clone the repo from git
# 2. create Python virtualenv and install dependencies
# 3. run your provisioning script

# enable pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# verify availability of python versions
pyenv versions

# install aws cli
pip3.8 install awscli --disable-pip-version-check
# install grc cli so we can git clone from codecommit
pip3.8 install git-remote-codecommit --disable-pip-version-check
# rehash pyenv so it will add awscli and grc to the path
pyenv rehash

# clone the git repo that contains your automation scripts
git clone codecommit::us-east-1://aws_ami_with_packer-project

# the current dir will be changed for all the following commands
cd aws_ami_with_packer-project || exit

# install necessary dependencies to pyenv python so we can run automation scripts
pip3.8 install -r requirements-automation.txt --disable-pip-version-check

# use automation scripts to create the virtualenv and install dependencies via poetry
python3.8 ./bin/s99_1_install_phase.py

# now you can use your virtualenv to run any complicated script
./.venv/bin/python ./amis/example/complicated_script.py
