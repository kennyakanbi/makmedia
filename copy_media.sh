#!/usr/bin/env bash
set -euo pipefail
mkdir -p /app/media
cp -r project/media/* /app/media/ 2>/dev/null || true
