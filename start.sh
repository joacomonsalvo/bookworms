#!/bin/bash

echo "──────────────────────────── Initializing BookWorms ────────────────────────────"

# Inicializa la web y luego ejecuta en el puerto de Render
reflex init --force

# Ejecuta Reflex en el puerto proporcionado por Render
reflex run --backend-host 0.0.0.0 --backend-port $PORT
