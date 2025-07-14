#!/bin/bash


echo "──────────────────────────── Starting BookWorms ────────────────────────────"

# Ejecutar Reflex en un solo proceso para backend + frontend
reflex run --frontend-host 0.0.0.0 --frontend-port $PORT
