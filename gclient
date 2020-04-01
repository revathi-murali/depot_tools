#!/usr/bin/env bash
# Copyright (c) 2009 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

base_dir=$(dirname "$0")

if [[ "#grep#fetch#cleanup#diff#setdep#" != *"#$1#"* ]]; then
  # Shall skip authomatic update?
  if [[ $DEPOT_TOOLS_UPDATE != 0 ]]; then
    echo "I am inside gclient code... DEPOT_TOOLS_UPDATE value is $DEPOT_TOOLS_UPDATE"
    "$base_dir"/update_depot_tools "$@"
    case $? in
      123)
        # msys environment was upgraded, need to quit.
        exit 0
        ;;
      0)
        ;;
      *)
        exit $?
    esac
  fi
fi

# Ensure that "depot_tools" is somewhere in PATH so this tool can be used
# standalone, but allow other PATH manipulations to take priority.
PATH=$PATH:$base_dir

# MINGW will equal 0 if we're running on Windows under MinGW.
MINGW=$(uname -s | grep MINGW > /dev/null; echo $?)

echo "I am inside gclient and this is the value of gclientpy3 - $GCLIENT_PY3 "

if [[ $GCLIENT_PY3 == 1 ]]; then
  echo "Gonna explicitly run on python3 and now I should go to vpython3"
  # Explicitly run on Python 3
  PYTHONDONTWRITEBYTECODE=1 exec vpython3 "$base_dir/gclient.py" "$@"
elif [[ $GCLIENT_PY3 == 0 ]]; then
  # Explicitly run on Python 2
  PYTHONDONTWRITEBYTECODE=1 exec vpython "$base_dir/gclient.py" "$@"
elif [[ $MINGW = 0 ]]; then
  # Run on Python 2 on Windows for now, allows default to be flipped.
  PYTHONDONTWRITEBYTECODE=1 exec vpython "$base_dir/gclient.py" "$@"
else
  # Run on Python 3, allows default to be flipped.
  PYTHONDONTWRITEBYTECODE=1 exec vpython3 "$base_dir/gclient.py" "$@"
fi
