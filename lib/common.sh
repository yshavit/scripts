#!/bin/bash

# To use this file within a script:
# 
#     CONFIG_NAME=yourscriptname source "$(dirname "$0")/lib/common.sh"
#
# You should hard-code CONFIG_NAME and never change it; that way, you'll keep your configs even if the script name changes.

set -euo pipefail

# if CONFIG_NAME is set:
# (1) create the config dir, if it's not already created
# (2) set its expanded path to $config_dir
# (3) define a function `config_file <name>`
if [ -n "${CONFIG_NAME:-}" ]; then
  config_dir="$HOME/.config/yshavit-scripts/$CONFIG_NAME"
  mkdir -p "$config_dir" || err "Couldn't create dir: $config_dir"

  function config_file() {
    if [ $# -ne 1 ] || [ -z "$1" ] ; then
      err "INTERNAL ERROR: bad arg to conf_file"
    fi
    echo "$config_dir/$1"
  }
fi

function msg() {
  local msg_text="$*"
  if [ -n "${COLOR-}" ]; then
    msg_text="\033[${COLOR}m${msg_text}\033[0m"
  fi
  >&2 echo -e "$msg_text"
}

function err() {
  msg "$@"
  exit 1
}

function is_installed() {
  command -v "$1" &>/dev/null
}

ys_scripts_home="$(dirname "$0")"
script_name="$(basename "$0")"

is_installed jq || err "Please install jq: brew install jq"
