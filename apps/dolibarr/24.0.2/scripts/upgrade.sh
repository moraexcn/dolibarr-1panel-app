#!/bin/sh
# Dolibarr requires install.lock to be removed before its container checks for
# a database migration. 1Panel runs this target-version script after stopping
# the old application and before starting the new Compose services.
# Source: https://github.com/Dolibarr/dolibarr-docker/blob/main/README.md#upgrading-dolibarr-version-and-migrating-db
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
app_dir=$(CDPATH= cd -- "$script_dir/.." && pwd -P)
documents_dir="$app_dir/data/documents"
lock_file="$documents_dir/install.lock"

if [ -L "$app_dir/data" ] || [ ! -d "$documents_dir" ] || [ -L "$documents_dir" ]; then
  echo "Dolibarr documents directory is missing or is a symlink: $documents_dir" >&2
  exit 1
fi
if [ -L "$lock_file" ] || { [ -e "$lock_file" ] && [ ! -f "$lock_file" ]; }; then
  echo "Dolibarr install.lock is not a regular file: $lock_file" >&2
  exit 1
fi

if [ -f "$lock_file" ]; then
  rm -f -- "$lock_file"
  echo "Removed Dolibarr install.lock before container upgrade."
else
  echo "Dolibarr install.lock is already absent."
fi
