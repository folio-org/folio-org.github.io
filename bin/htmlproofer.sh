#!/bin/bash

set -e

DEST="_site"

# Comma-separated string of regex patterns
IGNORE="/dev\.folio\.org/,/localhost:/"
IGNORE+=",/folio-org\/jenkins-pipeline-libs/"
IGNORE+=",/folio-org-priv\/folio-infrastructure/"
IGNORE+=",/folio-testing-okapi\.aws/"

# Ignore some known broken ones
IGNORE+=",/#mod-vendors/"

# Temporarily ignore github. Getting 429 error.
IGNORE+=",/github\.com\/folio-org/"

export NOKOGIRI_USE_SYSTEM_LIBRARIES=true

bundle exec jekyll build --trace

#  --log-level :debug
time bundle exec htmlproofer ./$DEST \
  --assume-extension \
  --allow-hash-href \
  --timeframe 6w \
  --url-ignore $IGNORE \
  $@

