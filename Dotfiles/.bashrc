### Colors and formatting variables
NORMAL="\[\033[m\]"
UNDERLINED="\e[4m"
BOLD="\[\033[1;30m\]"
RED_BOLD="\[\033[1;31m\]"
RED="\[\033[0;31m\]"
GREEN_BOLD="\[\033[1;32m\]"
GREEN="\[\033[0;32m\]"
BLUE_BOLD="\[\033[1;34m\]"
BLUE="\[\033[0;34m\]"

### Prompt format:
### 	user on hostname in [pwd]
###  	 >
if [[ $EUID -ne 0 ]]; then
	# Normal user prompt
	export PS1="\u on ${RED}\h${NORMAL} in [\w] ${NORMAL} \n > "
else
	# Root user prompt
	export PS1="${GREEN}\u${NORMAL} on ${RED}\h${NORMAL} in [\w] ${NORMAL} \n # "	
fi

export CLICOLOR=1
export LSCOLORS=ExFxBxDxCxegedabagacad

### History Settings
shopt -s histappend
export HISTCONTROL=ignoredups:ignorespace
export HISTTIMEFORMAT='%Y-%m-%dT%H:%M:%S  '
export HISTFILESIZE=500
export HISTSIZE=500

### Set path variables
export PATH="$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"
export PYTHONPATH="/Users/chris/Documents/Development/python-dev:$PYTHONPATH"

shopt -s checkwinsize
export EDITOR='subl'
export GCC_COLORS "error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01"
export JAVA_HOME=`/usr/libexec/java_home -v '1.8*'`

source ~/.aliases
