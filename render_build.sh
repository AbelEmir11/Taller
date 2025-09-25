#!/usr/bin/env bash
set -o errexit

# FRONTEND
npm install
npm run build

# BACKEND
pipenv install --deploy --ignore-pipfile

# Migraciones de base de datos
pipenv run flask db upgrade
