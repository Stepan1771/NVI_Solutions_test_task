#!/usr/bin/env bash

set -e

echo "Run apply migrations.."
alembic upgrade 40b6599eaf89
alembic upgrade 58818020c7e5
echo "Migrations applied!"

exec "$@"