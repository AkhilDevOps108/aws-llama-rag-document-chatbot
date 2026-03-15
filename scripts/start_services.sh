#!/usr/bin/env bash
set -euo pipefail

docker compose -f docker/docker-compose.yml up -d

echo "Qdrant and Redis are starting in the background."
echo "Run Ollama separately with: ollama serve"
echo "Then start the backend and frontend using the README instructions."

