#!/bin/bash

function config {
    /usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME $@
}

if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "SSH key exists"
else
    /usr/bin/ssh-keygen
    cat ~/.ssh/id_rsa.pub
    echo "Copy the SSH up to GitHub"
    echo
    echo
    read -n 1 -s -p "Press any key to continue"
fi

echo "!!!! Deploying config files !!!!"
git clone --bare git@github.com:suidroot/mydotfile.git $HOME/.cfg
mkdir -p .config-backup

echo "Backing up pre-existing dot files.";
config checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | xargs -I{} mv {} .config-backup/{}
config checkout
config config status.showUntrackedFiles no

echo "!!!! Installing tmux plugin manager !!!!"
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

echo "!!!! Installing BASH-IT !!!!"
git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it
~/.bash_it/install.sh

source $HOME/.bash_profile

bash-it enable plugin git tmux ssh
bash-it enable alias git fuck tmux

## Mac
if [ "$(uname)" == "Darwin" ]; then
    # Specify the preferences directory
    #defaults write com.googlecode.iterm2.plist PrefsCustomFolder -string "~/.iterm2"
    # Tell iTerm2 to use the custom preferences in the directory
    #defaults write com.googlecode.iterm2.plist LoadPrefsFromCustomFolder -bool true
    bash-it enable plugin osx
    bash-it enable alias homebrew osx

fi

