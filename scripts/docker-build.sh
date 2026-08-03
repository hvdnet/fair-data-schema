#!/usr/bin/env bash
set -euo pipefail

# Helper wrapper pointing to top-level docker-build.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

exec "${ROOT_DIR}/docker-build.sh" "$@"
