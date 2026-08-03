#!/usr/bin/env bash
set -euo pipefail

# Script: docker-build.sh
# Purpose: Build the FAIR Data JSON Schema API Docker container image
#          and save the exported image tarball archive into dist/

PUSH_IMAGE=false
SAVE_IMAGE=false

for arg in "$@"; do
  if [ "$arg" == "--push" ]; then
    PUSH_IMAGE=true
  elif [ "$arg" == "--save" ]; then
    SAVE_IMAGE=true
  fi
done

IMAGE_NAME="${IMAGE_NAME:-dartfx/fair-data-schema-api}"
TAG="${TAG:-latest}"
PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"
TAR_NAME="dartfx-fair-data-schema-api-docker.tar.gz"
DIST_DIR="$(pwd)/dist"

echo "=== Ensuring Docker Buildx Builder is Active ==="
if ! docker buildx inspect multiarch-builder >/dev/null 2>&1; then
  docker buildx create --name multiarch-builder --use >/dev/null 2>&1 || true
else
  docker buildx use multiarch-builder >/dev/null 2>&1 || true
fi

BUILD_ACTION=""
if [ "${PUSH_IMAGE}" = true ]; then
  BUILD_ACTION="--push"
fi

echo "=== Building Multi-Platform Docker Image: ${IMAGE_NAME}:${TAG} (${PLATFORMS}) ==="
if [ -n "${BUILD_ACTION}" ]; then
  docker buildx build --platform "${PLATFORMS}" -t "${IMAGE_NAME}:${TAG}" ${BUILD_ACTION} .
  echo "✓ Successfully built and pushed ${IMAGE_NAME}:${TAG} (${PLATFORMS}) to Docker Hub!"
else
  docker buildx build --platform "${PLATFORMS}" -t "${IMAGE_NAME}:${TAG}" .
  echo "✓ Successfully built ${IMAGE_NAME}:${TAG} (${PLATFORMS})"
fi

if [ "${SAVE_IMAGE}" = true ]; then
  mkdir -p "${DIST_DIR}"
  TAR_PATH="${DIST_DIR}/${TAR_NAME}"
  echo "=== Exporting Local Platform Image Archive to ${TAR_PATH} ==="
  docker buildx build -t "${IMAGE_NAME}:${TAG}" --load .
  docker save "${IMAGE_NAME}:${TAG}" | gzip > "${TAR_PATH}"
  echo "✓ Docker image ${IMAGE_NAME}:${TAG} successfully exported and saved to ${TAR_PATH}"
fi
