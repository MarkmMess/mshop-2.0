#!/usr/bin/env bash

set -e  # Остановить скрипт при любой ошибке

echo "certificate checking.."

CERTS_DIR="/app/src/certs"
PRIVATE_KEY="$CERTS_DIR/jwt-private.pem"
PUBLIC_KEY="$CERTS_DIR/jwt-public.pem"

if [ ! -f "$PRIVATE_KEY" ] || [ ! -f "$PUBLIC_KEY" ]; then
    mkdir -p "$CERTS_DIR"
    openssl genrsa -out "$PRIVATE_KEY" 2048
    openssl rsa -in "$PRIVATE_KEY" -outform PEM -pubout -out "$PUBLIC_KEY"
else
    echo "Certificates are available!"
fi

echo "Run apply migrations.."
alembic upgrade head
echo "Migrations applied!"

exec "$@"