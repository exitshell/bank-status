#!/usr/bin/env bash

USER="deploy"
ENV="prod"

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )

# Load HOST config.
source "$PARENT_PATH/hosts/$ENV/host.sh"

# Build private key location.
KEY="$PARENT_PATH/keys/$ENV/$ENV"

# ssh to remote host.
ssh -i $KEY $USER@$HOST $1
