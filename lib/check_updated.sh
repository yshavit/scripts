#!/bin/bash

# This script intentionally doesn't source lib/common.sh, because that invokes this,
# and we don't want to risk an infinite loop.
set -euo pipefail

cd "$(dirname "$0")"

git fetch origin main 2>/dev/null & # "&" means this may not get updated until next invocation, but that's okay

local_ahead_count="$(git rev-list --count origin/main..main)"
remote_ahead_count="$(git rev-list --count main..origin/main)"

function msg() {
  printf >&2 '\e[30;103m %s \e[0m\n' "$*"
}

if [ "$local_ahead_count" -ne 0 ]; then
  if [ "$remote_ahead_count" -ne 0 ]; then
    msg "scripts repo is $local_ahead_count ahead of origin and $remote_ahead_count behind."
  else
    msg "scripts repo is $local_ahead_count ahead of origin. Please push to origin."
  fi
elif [ "$remote_ahead_count" -ne 0 ]; then
  msg "scripts repo is $remote_ahead_count behind origin. Please pull from origin."
fi
