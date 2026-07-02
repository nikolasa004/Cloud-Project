#!/bin/bash

echo "Checking PostgreSQL..."

docker ps | grep pipeline_postgres

echo

echo "Checking Superset..."

docker ps | grep pipeline_superset

echo

curl http://localhost:8088/health