#!/bin/bash

set -e

DEST="_site"

# Comma-separated string of regex patterns
IGNORE="/dev\.folio\.org/,/localhost:/"
IGNORE+=",/folio-org\/jenkins-pipeline-libs/"
IGNORE+=",/folio-org-priv\/folio-infrastructure/"
IGNORE+=",/folio-snapshot-okapi\.dev/"
IGNORE+=",/folio-snapshot-test.*\/settings/"
IGNORE+=",/github\.com\/search/"
IGNORE+=",/github\.com\/pulls\/review-requested/"
IGNORE+=",/twitter\.com\//"
IGNORE+=",/folio\.org\/customization-hosting/"

# Ignore some known broken ones
IGNORE+=",/#mod-vendors/"

# Temporarily ignore github. Getting 429 error.
IGNORE+=",/github\.com\/folio-org/"

export NOKOGIRI_USE_SYSTEM_LIBRARIES=true

bundle exec jekyll build --trace

#  --log-level :debug
time bundle exec htmlproofer ./$DEST \
  --cache '{ "timeframe": { "external": "6w" } }' \
  --allow-missing-href=true \
  --ignore-urls $IGNORE \
  $@

