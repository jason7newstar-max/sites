#!/bin/bash
# Daily rebuild + redeploy of hinyc-db.
# Runs after auto-promote has had time to add new YT uploads.
set -e
SITE="$HOME/sites/hinyc-db"
LOG="$SITE/daily_rebuild.log"
TS=$(date +"%Y-%m-%dT%H:%M:%S%z")

cd "$SITE"

echo "[$TS] BUILD start" >> "$LOG"
python3 build.py >> "$LOG" 2>&1
echo "[$TS] BUILD done" >> "$LOG"

echo "[$TS] DEPLOY start" >> "$LOG"
# Use full path to npx (launchd PATH issues)
PATH="/Users/pinnyc/.local/bin:/usr/local/bin:/usr/bin:/bin" \
  /usr/local/bin/npx --yes vercel --prod --yes >> "$LOG" 2>&1
echo "[$TS] DEPLOY done" >> "$LOG"
