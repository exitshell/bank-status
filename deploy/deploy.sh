#!/usr/bin/env bash

USER="deploy"

# Get absolute path of the script.
PARENT_PATH=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
ROOT_PATH=$( cd "$(dirname "${PARENT_PATH}")" ; pwd -P )


# Check the existence of the env argument.
if [[ $# -eq 0 ]] ; then
    echo "Please specify an env (staging | prod)"
    exit
else
    # Get env argument.
    ENV=$1
    # Build private key location.
    KEY="$PARENT_PATH/keys/$ENV/$ENV"
    echo "  Using private key: $KEY"
fi

# If specified env directory exists, then make
# the same directories on the remote server.
if [ ! -f "$KEY" ]; then
    echo -e "\n\n! Private key: $KEY does not exist !"
    exit 1
fi


# Load HOST config.
source "$PARENT_PATH/hosts/$ENV/host.sh"
echo -e "-- Deploying application on $HOST --\n"


# Docker compose file location.
COMPOSE_PROD="/home/$USER/docker-compose-prod.yml"

# Pull docker images from docker hub registry.
PULL_CONTAINERS="docker-compose -f $COMPOSE_PROD pull"

# Stop existing containers.
STOP_CONTAINERS="docker-compose -f $COMPOSE_PROD stop -t 1"

# Remove existing volumes.
REMOVE_CONTAINERS="docker-compose -f $COMPOSE_PROD rm -fv"

# Recreate and start containers.
RESTART_CONTAINERS="docker-compose -f $COMPOSE_PROD up -d"

# Create deploy command.
DEPLOY_CMD=$(echo "$PULL_CONTAINERS && $STOP_CONTAINERS && $REMOVE_CONTAINERS && $RESTART_CONTAINERS")

# Execute deploy command.
ssh -i $KEY $USER@$HOST $DEPLOY_CMD

echo -e "\n-- Application has been deployed on $HOST --"
