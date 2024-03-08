#!/usr/bin/env bash

./translator.py examples/sources/hello.yaasm examples/bin/hello.json
./translator.py examples/sources/cat.yaasm examples/bin/cat.json
./translator.py examples/sources/prob1.yaasm examples/bin/prob1.json
./translator.py examples/sources/hello_user.yaasm examples/bin/hello_user.json