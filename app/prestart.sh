#!/bin/bash
export FLASK_APP=app/main.py
flask db migrate
flask db upgrade