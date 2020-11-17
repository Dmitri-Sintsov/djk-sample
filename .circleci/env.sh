#!/bin/bash
# Install pyenv to use exact version of Python.
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
pyenv init -
# pyenv install 3.9.0
echo Version of Python installed in the python:latest-browsers image.
python3 --version
# export PATH="$(pyenv root)/versions/3.9.0/bin/:$PATH"
echo Version of Python used to run the tests.
python3 --version
# https://stackoverflow.com/questions/27849412/permissionerror-with-pip3
python3 -m pip install -U pip wheel tox tox-pyenv setuptools pysqlite3 --user

