This is the source for "FOLIO Developers" at [dev.folio.org](https://dev.folio.org/)

To contribute changes, please refer to FAQs regarding [Developer documentation](https://dev.folio.org/faqs/#developer-documentation).

## Software requirements

Local development requires
[Ruby](https://www.ruby-lang.org/) and [Bundler](https://bundler.io/).
The 'bundle install' step will install the relevant local
[Jekyll](https://jekyllrb.com/).

For Ruby, using [rbenv](https://github.com/rbenv/rbenv) and its 'ruby-build'
plugin ensures a smooth process. In this directory, set the ruby version
with: `rbenv local 2.6.8`

Then do:

```
bundle config set --local path 'vendor/bundle'
bundle install
```

Occasionally a site maintainer will have updated dependencies,
and there will be changes to the `Gemfile.lock` file.
Do `bundle install` again.

## Docker

Instead of installing the requirements you may run
```
docker-compose up
```
to use the [Jekyll Docker image](https://github.com/envygeeks/jekyll-docker).

Our Gemfile defines the version of Jekyll that we use.

## Local development

To view and edit documents on your local machine, run the local Jekyll server:

```
bundle exec jekyll serve --port 5000
```

Then visit `localhost:5000` with the browser, and proceed to the page of interest.

Edit the relevant Markdown source document, and save it.
The server will automatically re-generate that particular page.
Now refresh the web browser to view its changes.

When finally ready with your set of changes, commit and push the branch to GitHub.
See [deployment](#deployment) notes below.

## Link checker

To verify internal and external links, do:

```
rake proof
```

or

```
bin/htmlproofer.sh
```

This will re-generate the whole site, then report any broken links.

Note that verification of GitHub links is disabled.

## Work area - management of dev site

See [notes](work/README.md) about the operation and management.
(Despite the name of this repository, it is not built using the GitHub tools.)

## Deployment

The master branch is automatically deployed as [dev.folio.org](https://dev.folio.org/)

Other branches are re-built upon push of changes. Follow the GitHub link from the branch's continuous-integration details to view the generated branch site.

## Additional information

Refer to FAQs regarding [Developer documentation](https://dev.folio.org/faqs/#developer-documentation) and [Raising Jira tickets](https://dev.folio.org/faqs/how-to-contribute-devdoc/#raising-jira-tickets).

The FOLIO [Slack](https://dev.folio.org/guidelines/which-forum/#slack) channel #dev-website

