#!/usr/bin/env bash
#
# backup_strategy.sh — Squelette d'une stratégie de sauvegarde DIFFÉRENCIÉE.
#
# Idée : ne pas tout sauvegarder de la même façon.
#   - Ce qui CHANGE SOUVENT (base de données + documents de travail) : léger, fréquent.
#   - Ce qui est LOURD ET STATIQUE (archives, médias) : sauvegarde unique, séparée.
#
# Ce fichier est un EXEMPLE : les chemins sont des placeholders (<...>), il n'exécute
# rien de réel tel quel. Adapter à son environnement avant usage.
#
set -euo pipefail

# --- Paramètres (à adapter) --------------------------------------------------
DEST="<dossier_de_sauvegarde>"          # p.ex. un disque dédié, hors du disque source
SOURCE_TRAVAIL="<dossier_documents>"    # ce qui change : documents de travail
DB_DUMP_CMD="<commande_de_dump_base>"   # p.ex. mysqldump --single-transaction ...
EXCLUDE="<dossier_lourd_a_exclure>"     # ce qu'on ne veut PAS dans la sauvegarde fréquente
RETENTION=3                             # nombre de sauvegardes conservées

STAMP="$(date +%Y%m%d_%H%M)"
mkdir -p "$DEST"

echo "[$(date)] Début de la sauvegarde différenciée"

# --- 1. Base de données (cohérente, compressée) ------------------------------
# $DB_DUMP_CMD | gzip > "$DEST/db_${STAMP}.sql.gz"

# --- 2. Documents de travail (on EXCLUT le lourd/statique) -------------------
# tar -C "$SOURCE_TRAVAIL" --exclude="$EXCLUDE" -cf - . \
#     | zstd -T2 -3 > "$DEST/travail_${STAMP}.tar.zst"

# --- 3. Rotation : on ne garde que les N dernières ---------------------------
# ls -t "$DEST"/db_*.sql.gz      2>/dev/null | tail -n +$((RETENTION + 1)) | xargs -r rm -f
# ls -t "$DEST"/travail_*.tar.zst 2>/dev/null | tail -n +$((RETENTION + 1)) | xargs -r rm -f

echo "[$(date)] Terminé."

# --- Règle d'or : une sauvegarde qu'on n'a pas TESTÉE n'est pas une sauvegarde.
# Vérifier régulièrement qu'une archive est lisible et restaurable :
#   zstd -dc "$DEST/travail_XXXX.tar.zst" | tar -tf - | head
#   zcat  "$DEST/db_XXXX.sql.gz" | head
#
# Et viser la règle 3-2-1 : 3 copies, 2 supports, 1 hors site.
