#!/usr/bin/env bash
set -euo pipefail

cp backend/.env.example backend/.env || true
cp frontend/.env.example frontend/.env || true

docker compose -f infrastructure/docker/docker-compose.yml up --build
