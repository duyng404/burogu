#!/bin/bash
python3 -m venv flask
source flask/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
