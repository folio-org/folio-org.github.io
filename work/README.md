# Work area - management of dev site

Some notes to assist with management of the dev.folio.org site.

* [Maintenance of dependencies](maintain-dependencies.md)
* [Maintenance of theme](maintain-theme.md)
* [Maintenance of search facilities](maintain-search.md)
* The site is built and deployed on every push to master branch. See the [note about new branches](../README.md#deployment)).

Some other useful explanations:
* [Guides](https://dev.folio.org/faqs/#developer-documentation) for updating documentation content.
* The [API documentation](https://dev.folio.org/reference/api/) and associated list of [endpoints](https://dev.folio.org/reference/api/endpoints/) navigation pages are generated from data files. See the Liquid code in the git source of those pages. The main data file is gathered by automated GitHub Workflows, as [explained](https://dev.folio.org/reference/api/#explain-gather-config).
* The [Source-code map](https://dev.folio.org/source-code/map/) navigation page is generated from data files. See the Liquid code in the git source of that page. See [explanation](https://dev.folio.org/source-code/map/#further-information) about how this map is assembled and maintained.

Old notes:

URL redirection: Some documentation links are in [FOLIO-966](https://issues.folio.org/browse/FOLIO-966).
(Note: It does not work properly.)

