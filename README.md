This is the source for "FOLIO Developers" at [dev.folio.org](https://dev.folio.org/)

To contribute changes, please make the changes in a new branch and submit a
pull request.

## Software requirements

Local development requires [curl](https://curl.haxx.se/) and
[Ruby](https://www.ruby-lang.org/) and [Bundler](https://bundler.io/).
The 'bundle install' step will install the relevant local
[Jekyll](https://jekyllrb.com/).

For Ruby, using [rbenv](https://github.com/rbenv/rbenv) and its 'ruby-build'
plugin ensures a smooth process. In this directory, set the ruby version
with: `rbenv local <version>`

Then do:

```
bundle install --path vendor/bundle
```

```
bundle exec jekyll serve --port 5000
```

```
bundle exec jekyll build
```

Occasionally do `bundle update` to advance the versions of dependencies.

## Docker

Instead of installing the requirements you may run
```
docker-compose up
```
to use the [Jekyll Docker image](https://github.com/envygeeks/jekyll-docker).

## Link checker

To verify internal and external links, do:

```
./bin/htmlproofer.sh
```

## Work area - management of dev site

See [notes](work/README.md).

## Deployment

The master branch is automatically deployed as [dev.folio.org](https://dev.folio.org/)

Other branches are re-built upon push of changes. Follow the GitHub link from the branch's continuous-integration details.

## Additional information

See project [FOLIO](https://issues.folio.org/browse/FOLIO)
at the [FOLIO issue tracker](https://dev.folio.org/guidelines/issue-tracker/).
We use the label "devweb" for items that relate to the software and facilities for building the website.
We use the label "devdoc" for items that relate to documentation content.

The FOLIO Slack channel #dev-website
