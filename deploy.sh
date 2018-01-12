#!/bin/bash
python3 -m venv flask
source flask/activate
pip install -r requirements.txt
deactivate
