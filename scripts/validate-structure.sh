#!/usr/bin/env bash
set -euo pipefail

echo "Checking repository structure..."
for path in apps/web apps/api packages/database/prisma .env.example README.md; do
  test -e "$path" || { echo "Missing $path"; exit 1; }
done

echo "Structure OK"
