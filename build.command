#! /bin/bash

pyinstaller --distpath ./bin --name elasticsearch-cli --onefile src/__main__.py
