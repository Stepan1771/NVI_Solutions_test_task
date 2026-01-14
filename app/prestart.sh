#!/usr/bin/env bash

set -e

echo "Run apply migrations.."
alembic upgrade b7219432ce66
alembic upgrade dde8e782246b
echo "Migrations applied!"

exec "$@"