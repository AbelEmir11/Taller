#!/usr/bin/env bash
set -o errexit

# FRONTEND
npm install
npm run build


# BACKEND
pip install -r requirements.txt

# Ejecutar migraciones en la DB de Render
flask db upgrade

# Arrancar la app con gunicorn (como está configurado en render.yaml)
gunicorn wsgi --chdir ./src/