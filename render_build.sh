#!/usr/bin/env bash
set -o errexit

# FRONTEND
npm install
npm run build

# BACKEND
pip install -r requirements.txt


