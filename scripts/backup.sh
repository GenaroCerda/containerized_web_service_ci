#!/usr/bin/env bash
set -euo pipefail

# --- Configuración (sobrescribible con variables de entorno) ---
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION="${RETENTION:-7}"          # cuántos backups conservar
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
FILE="${BACKUP_DIR}/miapi_${TIMESTAMP}.sql.gz"
TMP="${FILE}.tmp"

log() { echo "[$(date '+%F %T')] $*"; }

mkdir -p "$BACKUP_DIR"

# Si algo falla, borra el archivo parcial
trap 'rm -f "$TMP"' EXIT

log "Iniciando backup..."
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
  | gzip > "$TMP"

# Verifica que el archivo no esté vacío
if [ ! -s "$TMP" ]; then
  log "ERROR: el backup quedó vacío"
  exit 1
fi

mv "$TMP" "$FILE"
log "Backup creado: $FILE ($(du -h "$FILE" | cut -f1))"

# --- Rotación: conserva solo los últimos $RETENTION ---
ls -1t "$BACKUP_DIR"/miapi_*.sql.gz 2>/dev/null \
  | tail -n +"$((RETENTION + 1))" \
  | while read -r old; do
      log "Eliminando backup antiguo: $old"
      rm -f "$old"
    done

log "Listo."