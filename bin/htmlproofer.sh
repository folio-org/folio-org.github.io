#!/bin/bash

set -e

DEST="_site"

# Comma-separated string of regex patterns
IGNORE="/dev\.folio\.org/,/localhost:/"

export NOKOGIRI_USE_SYSTEM_LIBRARIES=true

bundle exec jekyll build --trace

#  --log-level :debug
time bundle exec htmlproofer ./$DEST \
  --assume-extension \
  --allow-hash-href \
  --timeframe 6w \
  --url-ignore $IGNORE \
  $@

