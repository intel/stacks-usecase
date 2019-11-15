#!/usr/bin/env bash

set -e
rm -rf pages

# generate docs
sphinx-build -b html docs pages
find pages/ -name \*.html -exec \
  sed -i 's/<span class="gp">\&gt;\&gt;\&gt; <\/span>//g' {} \;
find pages/ -name \*.html -exec \
  sed -i 's/<span class="go">\&gt;\&gt;\&gt;<\/span>//g' {} \;
cp -r docs/images pages/
touch pages/.nojekyll
