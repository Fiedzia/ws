#!/usr/bin/env bash
SCRIPTPATH="`dirname \"$0\"`"
. "$SCRIPTPATH/venv/bin/activate"
"$SCRIPTPATH/src/app.py" "$@"
