#!/bin/bash
clear
python3 -m venv virtual_env
source virtual_env/bin/activate
pip install --trusted-host https://pypi.python.org -r requirements.txt
clear
pytest Tests/
deactivate
