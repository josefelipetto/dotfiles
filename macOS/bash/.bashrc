### Colors and formatting variables
NORMAL="\033[0m"
UNDERLINED="\033[4m"
BOLD="\033[1;30m"
RED_BOLD="\033[1;31m"
RED="\033[0;31m"
GREEN_BOLD="\033[1;32m"
GREEN="\033[0;32m"
BLUE_BOLD="\033[1;34m"
BLUE="\033[0;34m"
YELLOW_BOLD="\033[1;33m"
YELLOW="\033[0;33m"

### Prompt format:
###   user on hostname in [pwd] git_branch_and_status
###    >
git_branch() {
  if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    return
  fi

  if [ -z "$(git status --short)" ]; then
    git_status_color="${GREEN}"
  else
    git_status_color="${YELLOW}"
  fi

  git_branch=`git --no-pager branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'`

  printf "${git_status_color}${git_branch}${git_status}${NORMAL}"
}

export PS1="\u on ${RED}\h${NORMAL} in [\w] \$(git_branch) \n > "

### History Settings
shopt -s histappend
export HISTCONTROL=ignoredups:ignorespace
export HISTTIMEFORMAT="%Y-%m-%dT%H:%M:%S  "
export HISTSIZE=50000

### Set environment variables
export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad
export PYTHONDONTWRITEBYTECODE=1
export EDITOR="nvim"
export GCC_COLORS="error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01"
export JAVA_HOME=`/usr/libexec/java_home -v '1.8*'`
export GOPATH="$HOME/Documents/Development/go"

### Set path variables
export PATH="$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:/usr/local/sbin:/usr/local/opt/texinfo/bin:/usr/local/opt/gettext/bin:$HOME/Library/Android/sdk/platform-tools:$HOME/Library/Android/sdk/tools:/opt/apache-maven-3.3.9/bin:$HOME/.composer/vendor/bin:$HOME/.pub-cache/bin:/Applications/Postgres.app/Contents/Versions/latest/bin:$GOPATH/bin:$HOME/.local/bin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"
export PYTHONPATH="$HOME/Documents/Development/python-dev:$PYTHONPATH"

### Shell optional behavior
shopt -s checkwinsize

### Additional aliases
source $HOME/.aliases

### Pyenv setup
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
source $HOME/.pyenv_versions

### Node Version Manager setup
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
