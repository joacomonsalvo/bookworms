#!/bin/bash

# Exportar variables de entorno si es necesario
# export VAR=value (o dejarlo para el panel de Render)

# Ejecuta el servidor Reflex en modo producción
reflex run --env prod --backend-only --loglevel info