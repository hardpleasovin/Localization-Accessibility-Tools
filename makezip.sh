#!/bin/sh
set -e
repo_name="localization-accessibility-tools"
zipfile="$repo_name.zip"
# remove previous zip
rm -f "$zipfile"
# gather files
zip -r "$zipfile" README.md LICENSE requirements.txt makezip.sh sample src .github
echo "Created $zipfile"
