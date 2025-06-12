#!/usr/bin/env bash
# Quick connectivity test for the Django backend API
# Usage: ./backend_check.sh [host] [port] [username] [password]

set -e

HOST=${1:-localhost}
PORT=${2:-8000}
USER=${3:-harsha}
PASS=${4:-harsha}

BASE_URL="http://${HOST}:${PORT}/api/accounts"

echo "Checking ${HOST}:${PORT}..."
if nc -z "$HOST" "$PORT"; then
  echo "\u2705 Port ${PORT} open"
else
  echo "\u274c Cannot connect to ${HOST}:${PORT}"
  exit 1
fi

echo "\nSending login request to ${BASE_URL}/login/ ..."
curl -i -X POST "${BASE_URL}/login/" \
  -H 'Content-Type: application/json' \
  -d "{\"username\": \"${USER}\", \"password\": \"${PASS}\"}"
