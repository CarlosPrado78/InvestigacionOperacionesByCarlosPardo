#!/usr/bin/env bash
# Ejecuta la aplicación desde el código fuente en macOS/Linux.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 main.py
