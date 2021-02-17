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
echo Environment used to run the tests
echo Kernel version
uname -a
echo System version
lsb_release -a
echo Python version
python3 --version
echo Chrome version
google-chrome --version
echo Chrome driver version
chromedriver --version
# https://stackoverflow.com/questions/27849412/permissionerror-with-pip3
python3 -m pip install -U pip wheel tox tox-pyenv setuptools pysqlite3 --user
