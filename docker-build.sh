#!/usr/bin/env bash
set -euo pipefail

# Script: docker-build.sh
# Purpose: Build the FAIR Data JSON Schema API Docker container image
#          and save the exported image tarball archive into dist/

IMAGE_NAME="${IMAGE_NAME:-fair-data-schema-api}"
TAG="${TAG:-latest}"
TAR_NAME="fair-data-schema-api-docker.tar.gz"
DIST_DIR="$(pwd)/dist"

echo "=== Building Docker Image: ${IMAGE_NAME}:${TAG} ==="
docker build -t "${IMAGE_NAME}:${TAG}" .

echo "=== Ensuring ${DIST_DIR} Directory Exists ==="
mkdir -p "${DIST_DIR}"

TAR_PATH="${DIST_DIR}/${TAR_NAME}"
echo "=== Saving Image Archive to ${TAR_PATH} ==="
docker save "${IMAGE_NAME}:${TAG}" | gzip > "${TAR_PATH}"

echo "✓ Docker image ${IMAGE_NAME}:${TAG} successfully built and saved to ${TAR_PATH}"
