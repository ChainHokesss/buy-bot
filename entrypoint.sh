#!/bin/sh

set -e

echo "Start service" && alembic upgrade head
exec python run.py
