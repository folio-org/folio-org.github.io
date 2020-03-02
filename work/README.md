# Work area - management of dev site

Some notes to assist with management of the dev.folio.org site.

* [Maintenance of dependencies](maintain-dependencies.md)
* [Maintenance of theme](maintain-theme.md)
* [Maintenance of search facilities](maintain-search.md)
* The site is built and deployed on every push to master or a branch.
The configuration and operation is a Static Builder Pipeline for AWS using Serverless,
[described](https://github.com/folio-org-priv/folio-infrastructure/tree/master/serverless-devdoc-pipeline) in the private folio-infrastructure repository.

URL redirection: Some documentation links are in [FOLIO-966](https://issues.folio.org/browse/FOLIO-966).
