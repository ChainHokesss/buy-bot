#!/bin/sh

set -e

echo "Start service" && make migrate
exec python run.py
