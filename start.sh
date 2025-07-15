#!/bin/bash

# (solo la primera vez) para recrear el web build
# Esto asegura que los archivos estáticos del frontend estén construidos.
reflex init || true

# Arranca Reflex en producción, poniendo FRONTEND y BACKEND en el mismo puerto
# Usamos '0.0.0.0' para que escuche en todas las interfaces de red, no solo localhost.
# La variable $PORT es proporcionada automáticamente por Render.
reflex run \
  --env prod \
  --loglevel info \
  --host 0.0.0.0 \
  --port $PORT