#!/bin/bash

set -euo pipefail

function msg() {
  >&2 echo "$@"
}

function err() {
  msg "$@"
  exit 1
}

function is_installed() {
  command -v "$1" &>/dev/null
}

ys_scripts_home="$(dirname "$0")"

is_installed jq || err "Please install jq: brew install jq"
