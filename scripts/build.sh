#!/bin/sh
# Copies only the public website into dist/ for the host to publish,
# leaving out editor config, docs and GitHub automation.
set -e
rm -rf dist
mkdir dist
cp -r index.html admin assets data dist/
echo "Built dist/"
