#!/usr/bin/env bash
set -euo pipefail

FILE="${1:?Uso: $0 <archivo.sql.gz>}"
[ -f "$FILE" ] || { echo "No existe: $FILE"; exit 1; }

echo "ATENCIÓN: esto reemplazará los datos actuales de la base."
read -r -p "Escribe 'si' para continuar: " ans
[ "$ans" = "si" ] || { echo "Cancelado."; exit 1; }

# Recrea el esquema public y carga el dump
docker compose exec -T db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'

gunzip -c "$FILE" | docker compose exec -T db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1'

echo "Restauración completada."