#!/bin/bash
# Rebuild worlds/<id> through the shared converter; sources default to the g2gfast inspirations folder.
export SRC="${SRC:-$HOME/godot/inspirations/g2gfast}"
exec "${DOTBSP_PATH:-$(dirname "$0")/../../dot-map-convert}/tools/regen_worlds.sh" "$(dirname "$0")/.." "$@"
