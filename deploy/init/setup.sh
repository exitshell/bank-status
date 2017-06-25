#!/usr/bin/env bash

USER="deploy"
ROOT_USER="root"
ROOT_HOME="/root"

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
    KEY="$ROOT_PATH/keys/$ENV/$ENV"
    echo "  Using private key: $KEY"
fi

# If specified env directory exists, then make
# the same directories on the remote server.
if [ ! -f "$KEY" ]; then
    echo -e "\n\n! Private key: $KEY does not exist !"
    exit 1
fi


# Load HOST config.
source "$ROOT_PATH/hosts/$ENV/host.sh"
echo -e "-- Provisioning server @ $HOST --\n"


# LOCKDOWN
# Copy '_lockdown.sh' script to the remote server.
echo -e "\n-- Copying lockdown script to remote server --"
LOCAL_LOCKDOWN_SCRIPT="$PARENT_PATH/_lockdown.sh"
REMOTE_LOCKDOWN_SCRIPT="$ROOT_HOME/_lockdown.sh"
scp -i $KEY $LOCAL_LOCKDOWN_SCRIPT $ROOT_USER@$HOST:$REMOTE_LOCKDOWN_SCRIPT

# Execute the 'lockdown.sh' script on remote server.
echo -e "\n-- Running lockdown script on remote server --"
ssh -i $KEY $ROOT_USER@$HOST sudo bash $REMOTE_LOCKDOWN_SCRIPT
sleep 2


# After the 'lockdown.sh' script runs, the user 'deploy'
# should be created with root privilages. We continue the
# server provision with the newly created user 'deploy.'


# INSTALL
# Copy '_install.sh' script to remote server.
echo -e "\n-- Copying install script to remote server --"
LOCAL_INSTALL_SCRIPT="$PARENT_PATH/_install.sh"
REMOTE_INSTALL_SCRIPT="/home/$USER/_install.sh"
scp -i $KEY $LOCAL_INSTALL_SCRIPT $USER@$HOST:$REMOTE_INSTALL_SCRIPT

# Execute 'install.sh' script on remote server.
echo -e "\n-- Running install script on remote server --"
ssh -i $KEY $USER@$HOST sudo bash $REMOTE_INSTALL_SCRIPT
ssh -i $KEY $USER@$HOST rm $REMOTE_INSTALL_SCRIPT


# MISC
# Add user 'deploy' to docker group.
echo -e "\n-- Adding user '$USER' to docker group on remote server --"
ssh -i $KEY $USER@$HOST sudo usermod -aG docker $USER

# Copy '_bash_profile' to remote server.
echo -e "\n-- Copying bash profile to remote server --"
LOCAL_BASH_PROFILE="$PARENT_PATH/_bash_profile"
REMOTE_BASH_PROFILE="/home/$USER/.bash_profile"
scp -i $KEY $LOCAL_BASH_PROFILE $USER@$HOST:$REMOTE_BASH_PROFILE


echo -e "\n-- Server @ $HOST has been provisioned --"
