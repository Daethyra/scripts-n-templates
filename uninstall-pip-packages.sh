#!/bin/bash
pip freeze --user | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip uninstall -y && sudo apt install python3-pip -y # && pip3 install -r requirements.txt