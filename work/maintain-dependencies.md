# Notes for maintaining site dependencies

Occasionally advance the versions of general dependencies
([FOLIO-1276](https://issues.folio.org/browse/FOLIO-1276)).

Do `bundle update --all` which will install the new versions
and will update the `Gemfile.lock` file.

Verify that the local site still renders properly.
If there was an update to Liquid, then verify the complex pages
such as "API documentation" and [Search](maintain-search.md).

If there are new versions of [Tocbot](https://github.com/tscanlin/tocbot)
then update the `_includes/head.html` file. There are two tocbot entries.
If neeeded, then there is other Tocbot configuration at the
`_includes/js-content.html` file.
Verify complex table-of-contents, such as "API documentation".

If there are new versions of [js-search](https://github.com/bvaughn/js-search)
then update the `_includes/head.html` file.
Verify [Search](maintain-search.md).

See other notes about [Maintenance of theme](maintain-theme.md).

