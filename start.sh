#!/bin/bash

echo "──────────────────────────── Starting BookWorms ────────────────────────────"

# Init si es necesario (opcional)
reflex init || true

# Build el frontend (si no está)
reflex export --frontend-only

# Ejecutar el backend con preview
reflex run --frontend-only --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 10000 --backend-only=false --loglevel debug --env prod
