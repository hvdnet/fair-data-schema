#!/usr/bin/env bash
set -euo pipefail

# Script: docker-build.sh
# Purpose: Build the FAIR Data JSON Schema API Docker container image
#          and save the exported image tarball archive into dist/

PUSH_IMAGE=false
SAVE_IMAGE=false
NO_CACHE=false

for arg in "$@"; do
  if [ "$arg" == "--push" ]; then
    PUSH_IMAGE=true
  elif [ "$arg" == "--save" ]; then
    SAVE_IMAGE=true
  elif [ "$arg" == "--no-cache" ]; then
    NO_CACHE=true
  fi
done

# Automatically enforce --no-cache when pushing or saving release builds
if [ "${PUSH_IMAGE}" = true ] || [ "${SAVE_IMAGE}" = true ]; then
  NO_CACHE=true
fi

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

BUILD_FLAGS=""
if [ "${NO_CACHE}" = true ]; then
  BUILD_FLAGS="--no-cache"
fi

if [ "${PUSH_IMAGE}" = true ]; then
  echo "=== Building & Pushing Multi-Platform Image: ${IMAGE_NAME}:${TAG} (${PLATFORMS}) ==="
  docker buildx build --platform "${PLATFORMS}" -t "${IMAGE_NAME}:${TAG}" ${BUILD_FLAGS} --push .
  echo "✓ Successfully built and pushed ${IMAGE_NAME}:${TAG} (${PLATFORMS}) to Docker Hub!"
else
  echo "=== Building Multi-Platform Docker Image: ${IMAGE_NAME}:${TAG} (${PLATFORMS}) ==="
  docker buildx build --platform "${PLATFORMS}" -t "${IMAGE_NAME}:${TAG}" ${BUILD_FLAGS} .
  echo "✓ Successfully built ${IMAGE_NAME}:${TAG} (${PLATFORMS})"
fi

if [ "${SAVE_IMAGE}" = true ]; then
  mkdir -p "${DIST_DIR}"
  TAR_PATH="${DIST_DIR}/${TAR_NAME}"
  echo "=== Exporting Local Platform Image Archive to ${TAR_PATH} ==="
  docker buildx build -t "${IMAGE_NAME}:${TAG}" ${BUILD_FLAGS} --load .
  docker save "${IMAGE_NAME}:${TAG}" | gzip > "${TAR_PATH}"
  echo "✓ Docker image ${IMAGE_NAME}:${TAG} successfully exported and saved to ${TAR_PATH}"
fi
