#!/bin/sh

echo "installing required python dependencies"
python3 -m venv pyenv
source pyenv/bin/activate
pip3 install -r requirements.txt

