#!/usr/bin/env bash
set -e

echo "[1/3] Building backend image..."
docker build -t xigua-ai-backend ./backend

echo "[2/3] Starting containers..."
docker compose up -d

echo "[3/3] Services started."
echo "Backend: http://localhost:8000/docs"
echo "Frontend: http://localhost:8080"
