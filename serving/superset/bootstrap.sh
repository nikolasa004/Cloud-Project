#!/bin/bash
set -e

echo "Waiting for Superset..."

until curl -sf http://localhost:8088/health >/dev/null
do
    sleep 5
done

echo "Running database migrations..."

docker exec pipeline_superset superset db upgrade

echo "Creating admin user..."

docker exec pipeline_superset superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password CloudProject2026! || true

echo "Initializing Superset..."

docker exec pipeline_superset superset init

echo "Superset initialized successfully."