#!/bin/bash

# (solo la primera vez) para recrear el web build
reflex init || true

# Arranca Reflex en producción, poniendo FRONTEND y BACKEND en el mismo puerto
reflex run \
  --env prod \
  --loglevel info \
  --backend-host 0.0.0.0 \
  --backend-port $PORT