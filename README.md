This is the source for "FOLIO Developers" at folio-org.github.io

To contribute changes, please make the changes in a new branch and submit a
pull request.

Local development requires [Jekyll](http://jekyllrb.com/) and
[Bundler](http://bundler.io/).

For Ruby, using [rbenv](https://github.com/rbenv/rbenv) and its 'ruby-build'
plugin ensures a smooth process. In this directory, set the ruby version
with: `rbenv local <version>`

Then do:

`$ bundle install --path vendor/bundle`

`$ bundle exec jekyll serve --port 5000`

`$ bundle exec jekyll build`

Occasionally do `bundle update` to advance the versions of dependencies.

If there is a need to override any more files, then copy them from the theme.
To find them, do: `bundle show minima`
