#!/usr/bin/env bash

USER="deploy"
ENV="prod"

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

# Update envs on remote server.
UPDATE_CMD="$PARENT_PATH/update.sh $ENV"

# Build application.
BUILD_CMD="$PARENT_PATH/build.sh $ENV"

# Deploy application to remote server.
DEPLOY_CMD="$PARENT_PATH/deploy.sh $ENV"

# Execute commands.
bash $UPDATE_CMD
bash $BUILD_CMD
bash $DEPLOY_CMD
