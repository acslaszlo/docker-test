#!/bin/bash

PYTONH_VER='python3.6'

virtualenv -p "${PYTONH_VER}" venv
virtualenv -p "${PYTONH_VER}" test-venv

. venv/bin/activate
pip install -r requirements.txt
