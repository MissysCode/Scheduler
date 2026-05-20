#!/usr/bin/env bash

set -euxo pipefail

REMOTE_SERVER="your-server"
REMOTE_APP_DIR="~/backend-scheduler"
REMOTE_STATIC_DIR="/var/www/html/scheduler"

echo "Running deployment dry run..."

rsync --dry-run --delete -av app/static/ \
    ${REMOTE_SERVER}:${REMOTE_STATIC_DIR}

rsync --dry-run \
    --exclude __pycache__ \
    --exclude venv \
    --exclude .git \
    --delete -av . \
    ${REMOTE_SERVER}:${REMOTE_APP_DIR}

read -p "Run actual deployment? (y/n): " confirm

if [[ $confirm == "y" ]]; then
    rsync --delete -av app/static/ \
        ${REMOTE_SERVER}:${REMOTE_STATIC_DIR}

    rsync \
        --exclude __pycache__ \
        --exclude venv \
        --exclude .git \
        --delete -av . \
        ${REMOTE_SERVER}:${REMOTE_APP_DIR}

    echo "Deployment completed successfully."
else
    echo "Deployment cancelled."
fi
